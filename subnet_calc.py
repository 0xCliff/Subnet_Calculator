# Starting with the network address (the given IP address, assuming it's the beginning of a subnet), increment by the subnet size (which is based on the new subnet mask) to get each new subnet. TODO

# Output: TODO
# Return the list of calculated subnets.
# Optionally, return the range of valid host addresses for each subnet, as well as the broadcast address for each subnet.

# A few points to consider:
# If you're working with CIDR notation (e.g., /24 for a subnet mask of 255.255.255.0), you'd adjust the CIDR prefix length instead of adjusting a default subnet mask.
# This algorithm does not consider the practical limitations of subnetting, such as the reservations for network and broadcast addresses.
# For a real-world application, ensure that you're handling edge cases and are accounting for the latest IP addressing practices and standards.

# This address, 192.168.1.0, is the network address for the subnet. Any IP address within this subnet will have the same result when ANDed with the subnet mask, which is how devices determine if another IP is within the same local network or if it's external and requires routing.

# This process is fundamental to IP routing. When a device needs to communicate with another IP address, it first determines if the target IP is on the same network or a different one by applying this process. If it's on the same network, it communicates directly; if it's on a different network, it forwards the data to the router.

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


def convert_new_mask_to_decimal(mask):
    octet_1 = int(mask[:8], 2)
    octet_2 = int(mask[8:16], 2)
    octet_3 = int(mask[16:24], 2)
    octet_4 = int(mask[24:], 2)

    return f"{octet_1}.{octet_2}.{octet_3}.{octet_4}"


def print_results(new_subnet):
    print(f"New subnet mask: {convert_new_mask_to_decimal(new_subnet)}")


def main():
    ip_addr = ipaddress.ip_address(args.ipAddress)
    default_subnet_mask = args.default_mask
    num_subnets = args.subnets or 1

    if args.ipAddress and ip_addr.is_private:
        subnet_class = determine_subnet_class(default_subnet_mask)
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
