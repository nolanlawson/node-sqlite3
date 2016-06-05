{
  "includes": [ "deps/common-sqlite.gypi" ],
  "variables": {
      "sqlite%"        : "internal",
      "sqlite_libname%": "sqlite3",
      "host%"          : "https://mapbox-node-binary.s3.amazonaws.com",
      "remote_path%"   : "./{name}/v{version}/{toolset}/",
      "package_name%"  : "{node_abi}-{platform}-{arch}.tar.gz"
  },
  "targets": [
    {
      "target_name": "node_sqlite3",
      "include_dirs": ["<!(node -e \"require('nan')\")"],
      "conditions": [
        ["sqlite != 'internal'", {
            "include_dirs": [ "<(sqlite)/include" ],
            "libraries": [
               "-l<(sqlite_libname)"
            ],
            "conditions": [ [ "OS=='linux'", {"libraries+":["-Wl,-rpath=<@(sqlite)/lib"]} ] ],
            "conditions": [ [ "OS!='win'", {"libraries+":["-L<@(sqlite)/lib"]} ] ],
            'msvs_settings': {
              'VCLinkerTool': {
                'AdditionalLibraryDirectories': [
                  '<(sqlite)/lib'
                ],
              },
            }
        },
        {
            "dependencies": [
              "deps/sqlite3.gyp:sqlite3"
            ]
        }
        ]
      ],
      "cflags": [ "-include ../src/gcc-preinclude.h" ],
      "sources": [
        "src/database.cc",
        "src/node_sqlite3.cc",
        "src/statement.cc"
      ]
    },
    {
      "target_name": "action_after_build",
      "type": "none",
      "dependencies": [ "node_sqlite3" ],
      "copies": [
          {
            "files": [ "<(PRODUCT_DIR)/node_sqlite3.node" ],
            "destination": "./lib/binding/{node_abi}-{platform}-{arch}"
          }
      ]
    }
  ]
}
