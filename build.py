#! python
# -*- coding: utf-8 -*-
#
# This file is part of the mimetypes library
#
# Copyright (c) 2023, zero.kwok@foxmail.com
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

import os
import re
import json
import copy
import platform
import mimetypes

mimetypes.init(files=None)

local = os.path.abspath(os.path.dirname(__file__))
items = copy.copy(mimetypes.types_map)
addin = {}
try:
    with open(os.path.join(local, 'collection.json'), 'rb') as f:
        addin = json.loads(f.read().decode())
except FileNotFoundError:
    addin = {
        ".m4a" : "audio/mp4",
        ".m4b" : "audio/mp4",
        ".m4p" : "audio/mp4",
        ".m4r" : "audio/mp4",
        ".m4v" : "video/mp4",
        ".m4u" : "video/vnd.mpegurl",
    }

items.update({key : addin[key] for key in addin if key not in items})
with open(os.path.join(local, 'collection.json'), 'wb') as f:
    f.write(json.dumps(items, indent=2, sort_keys=True).encode())
print(f'Original: {len(mimetypes.types_map)}, Additional: {len(addin)}, Output: {len(items)}')

header = '''\
// The file is automatically generated, changes will be overwritten, 
// from the mimetypes library.
//
// Copyright (c) 2023, zero.kwok@foxmail.com
// For the full copyright and license information, please view the LICENSE
// file that was distributed with this source code.

#ifndef mimetypes_h__
#define mimetypes_h__

#include <map>
#include <cctype>
#include <string>
#include <string.h>
#include <algorithm>
#include <filesystem>

namespace mimetypes {
namespace detail {

    struct const_strcmp {
        bool operator()(const char* a, const char* b) const {
            return strcmp(a, b) < 0;
        }
    };

    const static std::map<const char*, const char*, const_strcmp> __mimetypes =  {\
'''

footer = '''\
    }; // __mimetypes
} // namespace detail

inline std::string from_extension(const std::string& extension, bool strict = false)
{
    if (extension.empty())
        return strict ? "" : "application/octet-stream";

    auto _tolower = [](std::string s) -> std::string {
        std::transform(s.begin(), s.end(), s.begin(),
            [](unsigned char c) { return std::tolower(c); }
        );
        return s;
    };

    auto _get = [&](auto name) {
        auto item = detail::__mimetypes.find(_tolower(name));
        if (item != detail::__mimetypes.end())
            return item->second;
        return strict ? "" : "application/octet-stream";
    };

    if (extension[0] == '.' && extension.size() > 1)
        return _get(extension.c_str() + 1);
    else
        return _get(extension.c_str());
}

inline std::string from_filename(const std::filesystem::path& filename, bool strict = false) {
    return ::mimetypes::from_extension(filename.extension().u8string(), strict);
}

} // namespace mimetypes

#endif // mimetypes_h__
'''

items = sorted(items.items(), key=lambda x: (x[1], x[0]))
lines = re.split('\r\n|\n', header)

classes = set()
for k, v in items:
    v = v.lower()
    prefix = v[0 : v.find('/')]
    subfix = v[len(prefix) + 1: -1]
    if prefix not in classes:
        classes.add(prefix)
        lines.append('    ')
        lines.append(f'        // {prefix}')
    lines.append(f'        {{ "{k[1:]}", "{v}" }},')

lines += re.split('\r\n|\n', footer)

out = os.path.join(local, 'mimetypes.hpp')
ends = '\r\n' if platform.system() == 'Windows' else '\n'
with open(out, 'wb') as f:
    f.write(ends.join(lines).encode('utf-8'))

print(f'Write output to file: {out}')