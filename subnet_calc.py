# Input & Validate:
# Obtain the IP address. DONE
# Obtain the number of desired subnets (num_subnets). DONE
# Validate if the IP address is either an IPv4 or IPv6. DONE

# Determine Initial Subnet Mask: DONE
# Determine the default subnet mask for the given class of IP address.
# Class A: 1.0.0.0 to 126.0.0.0 -> Default subnet mask: 255.0.0.0
# Class B: 128.0.0.0 to 191.0.0.0 -> Default subnet mask: 255.255.0.0
# Class C: 192.0.0.0 to 223.0.0.0 -> Default subnet mask: 255.255.255.0
# (This assumes we're not considering the newer CIDR format)

# Calculate New Subnet Mask: DONE
# Convert the default subnet mask to binary. DONE
# Add bits to the subnet mask in the host portion (rightmost part) until you have enough subnets. Remember, for each bit you add, you double the number of subnets: 1 bit = 2 subnets, 2 bits = 4 subnets, 3 bits = 8 subnets, and so on. DONE
# Convert the new binary subnet mask back to decimal. DONE

# Generate Subnets: TODO
# Starting with the network address (the given IP address, assuming it's the beginning of a subnet), increment by the subnet size (which is based on the new subnet mask) to get each new subnet.

# Output: TODO
# Return the list of calculated subnets.
# Optionally, return the range of valid host addresses for each subnet, as well as the broadcast address for each subnet.

# A few points to consider:
# If you're working with CIDR notation (e.g., /24 for a subnet mask of 255.255.255.0), you'd adjust the CIDR prefix length instead of adjusting a default subnet mask.
# This algorithm does not consider the practical limitations of subnetting, such as the reservations for network and broadcast addresses.
# For a real-world application, ensure that you're handling edge cases and are accounting for the latest IP addressing practices and standards.

import argparse
import textwrap
import ipaddress
import math


def determine_subnet_class(subnet):
    if subnet == "255.0.0.0":
        return "A"
    elif subnet == "255.255.0.0":
        return "B"
    elif subnet == "255.255.255.0":
        return "C"
    else:
        raise ValueError("The subnet mask is not Valid")


def calculate_new_mask(subnet_class, nets):
    mask = ""
    additional_bits = math.ceil(math.log2(nets))

    if subnet_class == "A":
        mask += ("1" * (8 + additional_bits)) + ("0" * (24 - additional_bits))
    elif subnet_class == "B":
        mask += ("1" * (16 + additional_bits)) + ("0" * (16 - additional_bits))
    else:
        mask += ("1" * (24 + additional_bits)) + ("0" * (8 - additional_bits))

    return mask


def convert_mask_to_decimal(mask):
    octet_1 = mask[:8]
    octet_2 = mask[8:16]
    octet_3 = mask[16:24]
    octet_4 = mask[24:]

    return f"{int(octet_1, 2)}.{int(octet_2, 2)}.{int(octet_3, 2)}.{int(octet_4, 2)}"


def print_results(new_subnet):
    print(f"New subnet mask: {convert_mask_to_decimal(new_subnet)}")


def main():
    ip_addr = ipaddress.ip_address(args.ipAddress)
    binary_address = "{:#b}".format(ip_addr)[2:]
    default_subnet_mask = args.default_mask
    num_subnets = args.subnets or 1

    subnet_class = determine_subnet_class(default_subnet_mask)

    if args.ipAddress and ip_addr.is_private:
        if ip_addr.version == 4:
            subnet_mask = calculate_new_mask(subnet_class, num_subnets)
            print_results(subnet_mask)
        else:
            "{:#X}".format(ip_addr)
            print(ip_addr.compressed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Subnet Calculation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
            \033[92mpython subnet_calc.py\033[00m \033[96m-ip\033[00m 192.168.1.0 \033[96m-dm\033[00m 255.255.255.0 \033[96m-s\033[00m 4                         \033[31m# Calculate 4 subnets for 192.168.1.0\033[00m
            \033[92mpython subnet_calc.py\033[00m \033[96m--ipAddress\033[00m 10.1.0.0 \033[96m--default-mask\033[00m 255.0.0.0 \033[96m--subnets\033[00m 8      \033[31m# Calculate 8 subnets for 10.1.0.0\033[00m
            \033[92mpython subnet_calc.py\033[00m \033[96m-ip\033[00m 10.1.0.0 \033[96m--default-mask\033[00m 255.0.0.0 \033[96m-s\033[00m 2                     \033[31m# Calculate 2 subnets for 10.1.0.0\033[00m
        """
        ),
    )
    parser.add_argument(
        "-ip",
        "--ipAddress",
        help="Starting IP address",
        required=True,
        metavar="IP Address",
    )
    parser.add_argument(
        "-dm",
        "--default-mask",
        help="Default subnet mask",
        required=True,
        metavar="",
    )
    parser.add_argument(
        "-s",
        "--subnets",
        type=int,
        help="Number of subnets required",
        metavar="",
    )
    args = parser.parse_args()

    main()
