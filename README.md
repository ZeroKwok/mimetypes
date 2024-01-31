# mimetypes

mimetypes is a C++ library for mapping file extensions to MIME types. It provides a convenient way to determine the MIME type of a file based on its extension.

## Usage

Here is an example of how to use mimetypes in your C++ code:

```cpp
#include <iostream>
#include "mimetypes.hpp"

int main() {
    // Get MIME type from file extension
    std::string mimeType = mimetypes::from_extension(".txt"); // or "txt"
    std::cout << "MIME Type: " << mimeType << std::endl;

    // Get MIME type from filename
    std::string filename = "example.mp4";
    std::string mimeTypeFromFile = mimetypes::from_filename(filename);
    std::cout << "MIME Type from filename: " << mimeTypeFromFile << std::endl;

    return 0;
}
```

## Build

**Note**: The MIME type mappings in `mimetypes.hpp` are generated using Python's `mimetypes` module. You can update the mappings at any time by running the `build.py` script.

```py
python build.py
```

This will regenerate the `mimetypes.hpp` file with the latest MIME type mappings.
