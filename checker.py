import zlib
import sys

# png signature
PNG_SIGNATURE = b'\x89PNG\r\n\x1a\n'
CHUNK_SIZE_BYTES = 4
CHUNK_NAME_BYTES = 4
CHUNK_CRC_BYTES = 4

# calculates length of each scanline (row)
def calculate_scanline_length(ihdr_info):

    colortypes = {
        0: 1, # greyscale
        2: 3, # RGB
        3: -1, # PLTE # TODO: implement
        4: 2, # greyscale + alpha
        6: 4, # RGB + alpha
    }

    if ihdr_info['colortype'] == 3:
        print('[-] SORRY, not yet implemented for this colortype ;(')
        exit(-1)

    bits_per_pixel = ihdr_info['bitdepth'] * colortypes[ihdr_info['colortype']]
    bits_per_scanline = ihdr_info['width'] * bits_per_pixel

    return bits_per_scanline // 8 + 1

def analyze_ihdr(img, start):

    ihdr_info = {
        'width': int.from_bytes(img[start:start+4], byteorder='big'),
        'height': int.from_bytes(img[start+4:start+8], byteorder='big'),
        'bitdepth': int.from_bytes(img[start+8:start+9], byteorder='big'),
        'colortype': int.from_bytes(img[start+9:start+10], byteorder='big'),
        'compression': int.from_bytes(img[start+10:start:11], byteorder='big'),
        'filter': int.from_bytes(img[start+11:start+12], byteorder='big'),
        'interlaced': int.from_bytes(img[start+12:start+13], byteorder='big')
    }

    return ihdr_info

def main():

    if len(sys.argv) < 2:
        print('[*] usage: python {} <image file name>'.format(sys.argv[0]))
        exit(-1)

    img = open(sys.argv[1], 'rb').read()

    if img[:8] != PNG_SIGNATURE:
        print('Input file is not PNG')
        exit(-1)

    # analyze IHDR chunk
    ihdr_info = analyze_ihdr(img, img.index(b'IHDR') + CHUNK_NAME_BYTES)

    # find first IDAT chunk
    idat_start = img.index(b'IDAT') - CHUNK_SIZE_BYTES

    if idat_start < 0:
        print('Input file is invalid')
        exit(-1)

    compressed_img = b''
    while True:

        # get chunk size
        idat_content_size = int.from_bytes(img[idat_start:idat_start+CHUNK_SIZE_BYTES], byteorder='big')

        name_start = idat_start + CHUNK_SIZE_BYTES
        name_end = name_start + CHUNK_NAME_BYTES

        # if IDAT chunk ended, break
        if img[name_start:name_end] != b'IDAT':
            break

        content_start = idat_start + CHUNK_SIZE_BYTES + CHUNK_NAME_BYTES
        content_end = content_start + idat_content_size
        idat_chunk_content = img[content_start:content_end]

        # append all IDAT chunks
        compressed_img += idat_chunk_content

        # next chunk
        idat_start = content_end + CHUNK_CRC_BYTES

    # decompress the compressed image using DEFLATE algorithm
    decompressed_img = zlib.decompress(compressed_img)
    scanline_length = calculate_scanline_length(ihdr_info)
    real_height = len(decompressed_img) // scanline_length

    print('[*] Height in IHDR: {}'.format(hex(ihdr_info['height'])))
    print('[*] Real Height: {}'.format(hex(real_height)))

    if ihdr_info['height'] == real_height:
        print('[+] Size matches')
    else:
        print('[!!] Wrong size in IHDR')


if __name__ == '__main__':
    main()
