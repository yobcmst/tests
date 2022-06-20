from io import BytesIO, StringIO, UnsupportedOperation

from utils.functional import cached_property

class FileProxyMixin:
    """
    A mixin class used to forward file methods to an underlaying file
    object.  The internal file object has to be called "file"::
        class FileProxy(FileProxyMixin):
            def __init__(self, file):
                self.file = file
    """

    encoding = property(lambda self: self.file.encoding)
    fileno = property(lambda self: self.file.fileno)
    flush = property(lambda self: self.file.flush)
    isatty = property(lambda self: self.file.isatty)
    newlines = property(lambda self: self.file.newlines)
    read = property(lambda self: self.file.read)
    readinto = property(lambda self: self.file.readinto)
    readline = property(lambda self: self.file.readline)
    readlines = property(lambda self: self.file.readlines)
    seek = property(lambda self: self.file.seek)
    tell = property(lambda self: self.file.tell)
    truncate = property(lambda self: self.file.truncate)
    write = property(lambda self: self.file.write)
    writelines = property(lambda self: self.file.writelines)

    @property
    def closed(self):
        return not self.file or self.file.closed

    def readable(self):
        if self.closed:
            return False
        if hasattr(self.file, "readable"):
            return self.file.readable()
        return True

    def writable(self):
        if self.closed:
            return False
        if hasattr(self.file, "writable"):
            return self.file.writable()
        return "w" in getattr(self.file, "mode", "")

    def seekable(self):
        if self.closed:
            return False
        if hasattr(self.file, "seekable"):
            return self.file.seekable()
        return True

    def __iter__(self):
        return iter(self.file)


class File(FileProxyMixin):
    DEFAULT_CHUNK_SIZE = 64 * 2**10

    def __init__(self, file, name=None):
        self.file = file
        if name is None:
            name = getattr(file, "name", None)
        self.name = name
        if hasattr(file, "mode"):
            self.mode = file.mode

    def __str__(self):
        return self.name or ""

    def __repr__(self):
        return "<%s: %s>" % (self.__class__.__name__, self or "None")

    def __bool__(self):
        return bool(self.name)

    def __len__(self):
        return self.size

    @cached_property
    def size(self):
        if hasattr(self.file, "size"):
            return self.file.size
        if hasattr(self.file, "name"):
            try:
                return os.path.getsize(self.file.name)
            except (OSError, TypeError):
                pass
        if hasattr(self.file, "tell") and hasattr(self.file, "seek"):
            pos = self.file.tell()
            self.file.seek(0, os.SEEK_END)
            size = self.file.tell()
            self.file.seek(pos)
            return size
        raise AttributeError("Unable to determine the file's size.")

    def chunks(self, chunk_size=None):
        """
        Read the file and yield chunks of ``chunk_size`` bytes (defaults to
        ``File.DEFAULT_CHUNK_SIZE``).
        """
        chunk_size = chunk_size or self.DEFAULT_CHUNK_SIZE
        try:
            self.seek(0)
        except (AttributeError, UnsupportedOperation):
            pass

        while True:
            data = self.read(chunk_size)
            if not data:
                break
            yield data

    def multiple_chunks(self, chunk_size=None):
        """
        Return ``True`` if you can expect multiple chunks.
        NB: If a particular file representation is in memory, subclasses should
        always return ``False`` -- there's no good reason to read from memory in
        chunks.
        """
        return self.size > (chunk_size or self.DEFAULT_CHUNK_SIZE)

    def __iter__(self):
        # Iterate over this file-like object by newlines
        buffer_ = None
        for chunk in self.chunks():
            for line in chunk.splitlines(True):
                if buffer_:
                    if endswith_cr(buffer_) and not equals_lf(line):
                        # Line split after a \r newline; yield buffer_.
                        yield buffer_
                        # Continue with line.
                    else:
                        # Line either split without a newline (line
                        # continues after buffer_) or with \r\n
                        # newline (line == b'\n').
                        line = buffer_ + line
                    # buffer_ handled, clear it.
                    buffer_ = None

                # If this is the end of a \n or \r\n line, yield.
                if endswith_lf(line):
                    yield line
                else:
                    buffer_ = line

        if buffer_ is not None:
            yield buffer_

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, tb):
        self.close()

    def open(self, mode=None):
        if not self.closed:
            self.seek(0)
        elif self.name and os.path.exists(self.name):
            self.file = open(self.name, mode or self.mode)
        else:
            raise ValueError("The file cannot be reopened.")
        return self

    def close(self):
        self.file.close()

if __name__ == "__main__":
    path = "test_file/efair_nlp.txt"
    with open(path) as f:
        with File(f) as f_obj:
            out = f_obj.read()
    from IPython import embed; embed()