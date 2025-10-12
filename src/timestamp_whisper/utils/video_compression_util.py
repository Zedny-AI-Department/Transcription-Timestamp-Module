import zstandard as zstd


def compress_bytes(data: bytes) -> bytes:
    """
    Compresses a byte array using the zlib library.

    Args:
        data (bytes): The byte array to compress.

    Returns:
        bytes: The compressed byte array.
    """
    compressor = zstd.ZstdCompressor()
    return compressor.compress(data)


def decompress_bytes(compressed_data: bytes) -> bytes:
    """
    Decompresses a byte array using the zlib library.

    Args:
        compressed_data (bytes): The compressed byte array to decompress.

    Returns:
        bytes: The decompressed byte array.
    """
    decompressor = zstd.ZstdDecompressor()
    return decompressor.decompress(compressed_data)
