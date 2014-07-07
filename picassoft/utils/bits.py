# coding=utf-8

def get_bit_counter(bit_masks_num):
    """Generate bit mask count function.

    :param bit_masks_num: log2 of length in bits of a chunk
    :type bit_masks_num: int
    :return: generated function closure with bit masks
    :rtype: function

    Example:
    >>> get_bit_counter(13)(1000)
    6L
    """

    def generate_bit_masks(num):
        """Generate bit masks of the given length.

        :param num: log2 of length in bits of a mask
        :type num: int
        :return: generated masks
        :rtype: list of tuples
        """
        masks = []
        for i in xrange(num):
            shift = 1 << i
            mask = (1 << shift) - 1
            for x in xrange(num - i - 1):
                mask += mask << (shift << (x + 1))
            masks.append((shift, mask))
        return masks

    bit_masks = generate_bit_masks(bit_masks_num)
    bit_mask_len = 1 << bit_masks_num
    chunk_template = (1 << bit_mask_len) - 1

    def bit_count(value):
        """Count number of bits in the value.

        :param value: given value
        :type value: int or long
        :return: number of bits
        :rtype: int
        """
        count = 0
        while value > 0:
            chunk = value & chunk_template
            for shift, mask in bit_masks:
                chunk = (chunk & mask) + ((chunk >> shift) & mask)
            count += chunk
            value >>= bit_mask_len
        return count

    return bit_count

bit_count = get_bit_counter(12) # 4096 bits per chunk
