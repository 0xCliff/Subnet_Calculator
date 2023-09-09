# Input & Validate:
# Obtain the IP address. DONE
# Obtain the number of desired subnets (num_subnets). DONE
# Validate if the IP address is either an IPv4 or IPv6. DONE

# Determine Initial Subnet Mask: TODO
# Determine the default subnet mask for the given class of IP address.
# Class A: 1.0.0.0 to 126.0.0.0 -> Default subnet mask: 255.0.0.0
# Class B: 128.0.0.0 to 191.0.0.0 -> Default subnet mask: 255.255.0.0
# Class C: 192.0.0.0 to 223.0.0.0 -> Default subnet mask: 255.255.255.0
# (This assumes we're not considering the newer CIDR format)

# Calculate New Subnet Mask: TODO
# Convert the default subnet mask to binary. DONE
# Add bits to the subnet mask in the host portion (rightmost part) until you have enough subnets. Remember, for each bit you add, you double the number of subnets: 1 bit = 2 subnets, 2 bits = 4 subnets, 3 bits = 8 subnets, and so on.
# Convert the new binary subnet mask back to decimal.

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


def determine_subnet_class(subnet):
    pass


def calculate_new_mask(subnet):
    subnet = "{:#b}".format(subnet)[2:]  # Convert subnet mask to binary
    print(subnet)
    # print(subnet + 128)


def main():
    ip_addr = ipaddress.ip_address(args.ipAddress)
    binary_address = "{:#b}".format(ip_addr)[2:]
    subnet_mask = ipaddress.ip_address(args.default_mask)
    num_subnets = args.subnets

    subnet_class = determine_subnet_class(subnet_mask)

    if args.ipAddress and ip_addr.is_private:
        if ip_addr.version == 4:
            calculate_new_mask(subnet_class)
        else:
            "{:#X}".format(ip_addr)
            print(ip_addr.compressed)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Subnet Calculation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
            subnet_calc.py -ip 192.168.1.0 -m 255.255.255.0 -s 4                            # Calculate 4 subnets for 192.168.1.0
            subnet_calc.py --ipAddress 10.1.0.0 --default-mask 255.0.0.0 --subnets 8        # Calculate 8 subnets for 10.1.0.0
        """
        ),
    )
    parser.add_argument("-ip", "--ipAddress", help="Starting IP address")
    parser.add_argument("-m", "--default-mask", help="Default subnet mask")
    parser.add_argument("-s", "--subnets", type=int, help="Number of subnets required")
    args = parser.parse_args()

    main()
