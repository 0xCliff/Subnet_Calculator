import argparse
import textwrap
import ipaddress
import math

# fmt: off
CIDR_MAP = {
    (4, "255"): 32, (4, "254"): 31, (4, "252"): 30, (4, "248"): 29,
    (4, "240"): 28, (4, "224"): 27, (4, "192"): 26, (4, "128"): 25,
    (3, "255"): 24, (3, "254"): 23, (3, "252"): 22, (3, "248"): 21,
    (3, "240"): 20, (3, "224"): 19, (3, "192"): 18, (3, "128"): 17,
    (2, "255"): 16, (2, "254"): 15, (2, "252"): 14, (2, "248"): 13,
    (2, "240"): 12, (2, "224"): 11, (2, "192"): 10, (2, "128"): 9,
    (1, "255"): 8,  (1, "254"): 7,  (1, "252"): 6,  (1, "248"): 5,
    (1, "240"): 4,  (1, "224"): 3,  (1, "192"): 2,  (1, "128"): 1
}
# fmt: on


def reverse_CIDR_lookup(cidr):
    for k, v in CIDR_MAP.items():
        if cidr == v:
            return k


def get_subnet_CIDR(subnet):
    if subnet.startswith("/"):
        return reverse_CIDR_lookup(int(subnet[1:]))

    # Split the subnet and find the last non-zero octet.
    octets = subnet.split(".")
    octet_idx, slice_value = None, None
    for i, octet in enumerate(octets):
        if octet != "0":
            octet_idx = i + 1
            slice_value = octet

    if octet_idx is None:
        return None

    return (octet_idx, slice_value)


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


def make_final_address(ip, res, flag, pos):
    octets = ip.exploded.split(".")
    octets[pos - 1] = str(min(res, 255))

    for i in range(pos, len(octets)):
        if flag in [0, 1]:
            octets[i] = "0"
        elif flag in [-1, -2]:
            octets[i] = "255"

    if flag == 1:
        octets[-1] = str(int(octets[-1]) + 1)
    if flag == -2:
        octets[-1] = str(int(octets[-1]) - 1)

    address = ".".join(octets)
    return None if address == "255.0.0.0" else address


def get_details(ip, cidr, pos, subnet):
    octets = ip.exploded.split(".")
    octet = octets[pos - 1]
    group_size = 256 - subnet
    step = 0

    while step < int(octet) + 1:
        step += group_size

    details = {
        "network_id": make_final_address(ip, step - group_size, 0, pos),
        "broadcast_id": make_final_address(ip, step - 1, -1, pos),
        "first_host": make_final_address(ip, step - group_size, 1, pos),
        "last_host": make_final_address(ip, step - 1, -2, pos),
        "next_network": make_final_address(ip, step, 0, pos),
        "num_hosts": "{:,}".format(int(math.pow(2, (32 - cidr)) - 2)),
        "subnet_mask": f"{ip.exploded}/{cidr} -- {subnet}",
    }

    print_details(details)


def print_details(details):
    print(
        textwrap.dedent(
            f"""
                \033[92mNetwork ID:                         {details["network_id"]}
                Broadcast ID:                       {details["broadcast_id"]}
                First network host:                 {details["first_host"]}
                Last network host:                  {details["last_host"]}
                Next network:                       {details["next_network"]}
                # of usable hosts p/subnet:         {details["num_hosts"]}
                Subnet mask:                        {details["subnet_mask"]}\033[00m
            """
        )
    )


def main():
    ip_addr = ipaddress.ip_address(args.ipAddress)
    subnet_mask = args.mask
    num_subnets = args.subnets
    details = args.get_details
    calc = args.calculate

    if details:
        if ip_addr.version == 4:
            octet_position, subnet = get_subnet_CIDR(subnet_mask)
            get_details(
                ip_addr,
                CIDR_MAP[get_subnet_CIDR(subnet_mask)],
                octet_position,
                int(subnet),
            )

    if calc:
        if ip_addr.version == 4:
            pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        prog="subnet_calc.py",
        description="Subnet Calculation Tool",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=textwrap.dedent(
            """Example:
    \033[92mpython subnet_calc.py\033[00m \033[96m-g\033[00m \033[96m-i\033[00m 192.168.1.0 \033[96m-m\033[00m /24                                   \033[31m# get all deatils about network for 192.168.1.0/24\033[00m
    \033[92mpython subnet_calc.py\033[00m \033[96m-c\033[00m \033[96m--ipAddress\033[00m 10.1.0.0 \033[96m--mask\033[00m 255.0.0.0 \033[96m--subnets\033[00m 8      \033[31m# Calculate 8 subnets for 10.1.0.0\033[00m
    \033[92mpython subnet_calc.py\033[00m \033[96m-c\033[00m \033[96m-i\033[00m 10.1.0.0 \033[96m--mask\033[00m 255.0.0.0 \033[96m-s\033[00m 2                      \033[31m# Calculate 2 subnets for 10.1.0.0\033[00m
        """
        ),
        usage="\033[92mpython subnet_calc.py\033[00m \033[96m-g\033[00m \033[96m-i\033[00m 192.168.1.0 \033[96m-m\033[00m 24",
    )
    parser.add_argument(
        "-g",
        "--get-details",
        help="Get all network details for given IP and Subnet mask",
        action="store_true",
    )
    parser.add_argument(
        "-c",
        "--calculate",
        help="Calculate network details for given IP and # of subnets needed",
        action="store_true",
    )
    parser.add_argument(
        "-i",
        "--ipAddress",
        help="IP address",
        required=True,
        metavar="\b",
    )
    parser.add_argument(
        "-m",
        "--mask",
        help="Subnet mask or CIDR",
        metavar="\b",
    )
    parser.add_argument(
        "-s",
        "--subnets",
        type=int,
        help="Number of subnets required",
        default=1,
        metavar="\b",
    )
    args = parser.parse_args()

    main()
