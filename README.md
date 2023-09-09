# Subnet Calculator

Alright, here's the deal: I've got a good grasp on subnetting formulas. So much so, I can do the math in about a minute by hand. Funny enough, coding it took a bit longer than if I'd just calculated a thousand networks the old-fashioned way. But hey, that's the fun of side projects during coursework! I genuinely enjoy both programming and networking, and it'd be pretty cool to mesh those two passions in my professional journey down the road - Jakob Johnson - jakob.johnson.dev@gmail.com

## The Tool

Subnet Calculator is a tool with two main functions:

- Provides details about a given IP and subnet mask or CIDR notation:

  - details include:
    - Network address
    - Broadcast Address
    - First host
    - Last host
    - Next network address
    - \# of usable IP addresses
    - The subnet mask in in dot and CIDR notation

- Calculate subnets based on a given IP address and the number of desired subnets.

This tool primarily focuses on IPv4 addressing with the goal of adding IPv6 support.

## Features

- Get details about your network from the IP and subnet mask
- Calculate subnet mask based on the desired # of subnets.
- List all possible subnets.
- Determine valid host ranges and broadcast address for each subnet.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- A machine running a Unix-like OS or Windows.
- Basic knowledge of IP addressing.

## Usage

- Run the command: `python subnet_calc.py -h`
- It's really not that complicated

## License

Subnet_Calculator License

Copyright (c) 2023, Jakob Johnson

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
