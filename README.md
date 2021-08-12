# lihim
**(WIP)** CLI for managing secret keys, tokens, sensitive and/or public key-value pairs. AKA *"A note-taking CLI tool glorified with added security and complexity for listing key-value pairs."*

## Overview
**Lihim** (Filipino word for *secret*) uses PyNaCl for secret key encryption, and stores the key-value pairs in an SQLite/PostgreSQL database. Secret keys are managed according to users and groups. That is, each user has groups and these groups can contain several key-value pairs.

![lihim-chart](https://res.cloudinary.com/nvqacloud/image/upload/v1628687874/lihim_chart_nwir6s.png)

## License
MIT License

Copyright (c) 2021 Neil Van

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.