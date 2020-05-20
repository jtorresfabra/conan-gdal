import glob
import os

from conans import ConanFile, AutoToolsBuildEnvironment, tools

class GdalConan(ConanFile):
    name = "gdal"
    description = "GDAL is an open source X/MIT licensed translator library " \
                  "for raster and vector geospatial data formats."
    license = "MIT"
    topics = ("conan", "gdal", "osgeo", "geospatial", "raster", "vector")
    homepage = "https://github.com/OSGeo/gdal"
    url = "https://github.com/conan-io/conan-center-index"
    exports_sources = "patches/**"
    generators = "pkg_config"
    settings = "os", "arch", "compiler", "build_type"
    options = {
        "shared": [True, False],
        "fPIC": [True, False],
        "simd_intrinsics": [None, "sse", "ssse3", "avx"],
        "threadsafe": [True, False],
        "with_zlib": [True, False],
        "with_zstd": [True, False],
        "with_pg": [True, False],
        # "with_libgrass": [True, False],
        "with_cfitsio": [True, False],
        "with_pcraster": [True, False],
        "with_png": [True, False],
        # "with_dds": [True, False],
        "with_gta": [True, False],
        "with_pcidsk": [True, False],
        "with_jpeg": [True, False],
        "with_charls": [True, False],
        "with_gif": [True, False],
        # "with_ogdi": [True, False],
        # "with_sosi": [True, False],
        # "with_mongocxx": [True, False],
        "with_hdf4": [True, False],
        "with_hdf5": [True, False],
        # "with_kea": [True, False],
        # "with_netcdf": [True, False],
        "with_jasper": [True, False],
        "with_openjpeg": [True, False],
        # "with_fgdb": [True, False],
        "with_gnm": [True, False],
        # "with_mysql": [True, False],
        "with_xerces": [True, False],
        "with_expat": [True, False],
        "with_libkml": [True, False],
        "with_odbc": [True, False],
        # "with_dods_root": [True, False],
        "with_curl": [True, False],
        "with_xml2": [True, False],
        # "with_spatialite": [True, False],
        "with_sqlite3": [True, False],
        # "with_rasterlite2": [True, False],
        "with_pcre": [True, False],
        # "with_epsilon": [True, False],
        "with_webp": [True, False],
        "with_geos": [True, False],
        # "with_sfcgal": [True, False],
        "with_qhull": [True, False],
        # "with_opencl": [True, False],
        # "with_freexl": [True, False],
        "without_pam": [True, False],
        "enable_pdf_plugin": [True, False],
        # "with_poppler": [True, False],
        # "with_podofo": [True, False],
        # "with_pdfium": [True, False],
        # "with_tiledb": [True, False],
        # "with_rasdaman": [True, False],
        # "with_armadillo": [True, False],
        # "with_cryptopp": [True, False],
        "with_crypto": [True, False],
        "without_lerc": [True, False],
        "with_null": [True, False],
        "with_exr": [True, False],
    }
    default_options = {
        "shared": False,
        "fPIC": True,
        "simd_intrinsics": "sse",
        "threadsafe": True,
        "with_zlib": True,
        "with_zstd": True,
        "with_pg": True,
        # "with_libgrass": True,
        "with_cfitsio": True,
        "with_pcraster": True,
        "with_png": True,
        # "with_dds": False,
        "with_gta": True,
        "with_pcidsk": True,
        "with_jpeg": True,
        "with_charls": True,
        "with_gif": True,
        # "with_ogdi": True,
        # "with_sosi": False,
        # "with_mongocxx": True,
        "with_hdf4": True,
        "with_hdf5": True,
        # "with_kea": True,
        # "with_netcdf": True,
        "with_jasper": True,
        "with_openjpeg": True,
        # "with_fgdb": True,
        "with_gnm": True,
        # "with_mysql": False,
        "with_xerces": True,
        "with_expat": True,
        "with_libkml": True,
        "with_odbc": False, # default should be True but odbc conan recipe doesn't support Windows yet
        # "with_dods_root": False,
        "with_curl": True,
        "with_xml2": True,
        # "with_spatialite": False,
        "with_sqlite3": True,
        # "with_rasterlite2": False,
        "with_pcre": True,
        # "with_epsilon": False,
        "with_webp": True,
        "with_geos": True,
        # "with_sfcgal": True,
        "with_qhull": True,
        # "with_opencl": False,
        # "with_freexl": True,
        "without_pam": False,
        "enable_pdf_plugin": False,       # to test (libtool must be disabled)
        # "with_poppler": False,
        # "with_podofo": False,
        # "with_pdfium": False,
        # "with_tiledb": True,
        # "with_rasdaman": False,
        # "with_armadillo": False,
        # "with_cryptopp": True,
        "with_crypto": False,
        "without_lerc": False,
        "with_null": False,
        "with_exr": True,
    }
    requires = [("libiconv/1.16", "override")] # just to fix conflicts

    _autotools= None

    @property
    def _source_subfolder(self):
        return "source_subfolder"

    @property
    def _build_subfolder(self):
        return "build_subfolder"

    def config_options(self):
        if self.settings.os == "Windows":
            del self.options.fPIC

    def configure(self):
        if self.settings.compiler.cppstd:
            tools.check_min_cppstd(self, 11)
        if self.settings.arch not in ["x86", "x86_64"]:
            del self.options.simd_intrinsics
        if self.options.without_lerc:
            del self.options.with_zstd
        # if self.options.with_spatialite:
        #     del self.options.with_sqlite3
        if not self.options.get_safe("with_sqlite3", False):
            del self.options.with_pcre
        # if tools.Version(self.version) < "3.0.0":
        #     del self.options.with_tiledb
        if tools.Version(self.version) < "3.1.0":
            del self.options.with_exr

    # def build_requirements(self):
    #     if self.settings.os == "Linux":
    #         self.build_requires("autoconf/2.69")

    def requirements(self):
        self.requires("json-c/0.13.1")
        self.requires("libgeotiff/1.5.1")
        self.requires("libtiff/4.1.0")
        self.requires("proj/7.0.0")
        if tools.Version(self.version) >= "3.1.0":
            self.requires("flatbuffers/1.12.0")
        if self.options.with_zlib:
            self.requires("zlib/1.2.11")
        if self.options.get_safe("with_zstd"):
            self.requires("zstd/1.4.4")
        if self.options.with_pg:
            self.requires("libpq/11.5")
        # if self.options.with_libgrass:
        #     self.requires("libgrass/x.x.x")
        if self.options.with_cfitsio:
            self.requires("cfitsio/3.470")
        # if self.options.with_pcraster:
        #     self.requires("pcraster-rasterformat/x.x.x")
        if self.options.with_png:
            self.requires("libpng/1.6.37")
        # if self.options.with_dds:
        #     self.requires("crunch/x.x.x")
        if self.options.with_gta:
            self.requires("libgta/1.2.1")
        # if self.options.with_pcidsk:
        #     self.requires("pcidsk/x.x.x")
        if self.options.with_jpeg:
            self.requires("libjpeg/9d")
        if self.options.with_charls:
            self.requires("charls/2.1.0")
        if self.options.with_gif:
            self.requires("giflib/5.1.4")
        # if self.options.with_ogdi:
        #     self.requires("ogdi/4.1.0")
        # if self.options.with_sosi:
        #     self.requires("fyba/4.1.1")
        # if self.options.with_mongocxx:
        #     self.requires("mongocxx/x.x.x")
        if self.options.with_hdf4:
            self.requires("hdf4/4.2.15")
        if self.options.with_hdf5:
            self.requires("hdf5/1.12.0")
        # if self.options.with_netcdf:
        #     self.requires("netcdf-c/x.x.x")
        if self.options.with_jasper:
            self.requires("jasper/2.0.16")
        if self.options.with_openjpeg:
            self.requires("openjpeg/2.3.1")
        # if self.options.with_fgdb:
        #     self.requires("file-geodatabase-api/x.x.x")
        # if self.options.with_mysql:
        #     self.requires("xxxx/x.x.x") # which one to use?
        if self.options.with_xerces:
            self.requires("xerces-c/3.2.2")
        if self.options.with_expat:
            self.requires("expat/2.2.9")
        if self.options.with_libkml:
            self.requires("libkml/1.3.0")
        if self.options.with_odbc:
            self.requires("odbc/2.3.7")
        # if self.options.with_dods_root:
        #     self.requires("libdap/x.x.x")
        if self.options.with_curl:
            self.requires("libcurl/7.69.1")
        if self.options.with_xml2:
            self.requires("libxml2/2.9.10")
        # if self.options.with_spatialite:
        #     self.requires("spatialite/x.x.x")
        if self.options.get_safe("with_sqlite3"):
            self.requires("sqlite3/3.31.1")
        # if self.options.with_rasterlite2:
        #     self.requires("rasterlite2/x.x.x")
        if self.options.get_safe("with_pcre"):
            self.requires("pcre/8.41")
        # if self.options.with_epsilon:
        #     self.requires("epsilon/0.9.2")
        if self.options.with_webp:
            self.requires("libwebp/1.1.0")
        if self.options.with_geos:
            self.requires("geos/3.8.1")
        # if self.options.with_sfcgal:
        #     self.requires("sfcgal/1.3.7")
        # if self.options.with_qhull:
        #     self.requires("qhull/x.x.x")
        # if self.options.with_opencl:
        #     self.requires("opencl-headers/x.x.x")
        # if self.options.with_freexl:
        #     self.requires("freexl/x.x.x")
        # if self.options.with_poppler:
        #     self.requires("poppler/x.x.x")
        # if self.options.with_podofo:
        #     self.requires("podofo/x.x.x")
        # if self.options.with_pdfium:
        #     self.requires("pdfium/x.x.x")
        # if self.options.get_safe("with_tiledb"):
        #     self.requires("tiledb/x.x.x")
        # if self.options.with_rasdaman:
        #     self.requires("raslib/x.x.x")
        # if self.options.with_armadillo:
        #     self.requires("armadillo/x.x.x")
        # if self.options.with_cryptopp:
        #     self.requires("cryptopp/x.x.x")
        if self.options.with_crypto:
            self.requires("openssl/1.1.1g")
        # if not self.options.without_lerc:
        #     self.requires("lerc/2.1") # TODO: use conan recipe (not possible yet because lerc API is broken for GDAL)
        if self.options.get_safe("with_exr"):
            self.requires("openexr/2.4.0")

    def source(self):
        tools.get(**self.conan_data["sources"][self.version])
        os.rename(self.name + "-" + self.version, self._source_subfolder)

    def _configure_autotools(self):
        if self._autotools:
            return self._autotools
        configure_dir=os.path.join(self._source_subfolder, "gdal")
        with tools.chdir(configure_dir):
            self.run("autoconf -i")
        self._autotools = AutoToolsBuildEnvironment(self)

        args = []
        # Shared/Static
        if self.options.shared:
            args.extend(["--disable-static", "--enable-shared"])
        else:
            args.extend(["--disable-shared", "--enable-static"])
        # Debug
        if self.settings.build_type == "Debug":
            args.append("--enable-debug")
        # SIMD Intrinsics
        simd_intrinsics = self.options.get_safe("simd_intrinsics", False)
        if not simd_intrinsics:
            args.extend(["--without-sse", "--without-ssse3", "--without-avx"])
        elif simd_intrinsics == "sse":
            args.extend(["--with-sse", "--without-ssse3", "--without-avx"])
        elif simd_intrinsics == "ssse3":
            args.extend(["--with-sse", "--with-ssse3", "--without-avx"])
        elif simd_intrinsics == "avx":
            args.extend(["--with-sse", "--with-ssse3", "--with-avx"])
        # LTO (disabled)
        args.append("--disable-lto")
        # 
        args.append("--with-hide_internal_symbols")
        args.append("--without-rename-internal-libtiff-symbols")
        args.append("--without-rename-internal-libgeotiff-symbols")
        args.append("--with-rename-internal-shapelib-symbols") # we use internal shapelib, so symbols are renamed
        #
        args.append("--without-local")
        # Threadsafe
        args.append("--with-threads={}".format("yes" if self.options.threadsafe else "no"))
        # Mandatory dependencies:
        args.append("--with-proj=yes")
        # Optional dependencies:
        args.append("--with-libz={}".format("yes" if self.options.with_zlib else "no"))
        args.append("--with-liblzma=no") # liblzma is an optional transitive dependency of gdal (through libtiff).
        args.append("--with-zstd={}".format("yes" if self.options.get_safe("with_zstd") else "no")) # Optional direct dependency of gdal only if lerc lib enabled
        # Drivers:
        if not (self.options.with_zlib and self.options.with_png and self.options.with_jpeg):
            args.append("--disable-driver-mrf") # MRF raster driver depends on zlib, libpng and libjpeg
        args.append("--with-pg={}".format("yes" if self.options.with_pg else "no"))
        args.extend(["--without-grass", "--without-libgrass"]) # TODO: to implement when libgrass lib available
        args.append("--with-cfitsio={}".format(self.deps_cpp_info["cfitsio"].rootpath if self.options.with_cfitsio else "no"))
        args.append("--with-pcraster={}".format("internal" if self.options.with_pcraster else "no")) # TODO: use conan recipe when available instead of internal one
        args.append("--with-png={}".format(self.deps_cpp_info["libpng"].rootpath if self.options.with_png else "no"))
        args.append("--without-dds") # TODO: to implement when crunch lib available
        args.append("--with-gta={}".format(self.deps_cpp_info["libgta"].rootpath if self.options.with_gta else "no"))
        args.append("--with-pcidsk={}".format("internal" if self.options.with_pcidsk else "no")) # TODO: use conan recipe when available instead of internal one
        args.append("--with-libtiff=yes") # libtiff (required !)
        args.append("--with-geotiff=yes") # libgeotiff (required !)
        args.append("--with-jpeg={}".format(self.deps_cpp_info["libjpeg"].rootpath if self.options.with_jpeg else "no"))
        args.append("--without-jpeg12") # it requires internal libjpeg and libgeotiff
        args.append("--with-charls={}".format("yes" if self.options.with_charls else "no"))
        args.append("--with-gif={}".format(self.deps_cpp_info["giflib"].rootpath if self.options.with_gif else "no"))
        args.append("--without-ogdi") # TODO: to implement when ogdi lib available (https://sourceforge.net/projects/ogdi/)
        args.append("--without-fme") # commercial library
        args.append("--without-sosi") # TODO: to implement when fyba lib available
        args.append("--without-mongocxx") # TODO: to implement when mongocxx lib available
        args.append("--with-hdf4={}".format("yes" if self.options.with_hdf4 else "no"))
        args.append("--with-hdf5={}".format("yes" if self.options.with_hdf5 else "no"))
        args.append("--without-kea") # TODO: to implement when kealib available
        args.append("--without-netcdf") # TODO: to implement when netcdf-c lib available
        args.append("--with-jasper={}".format(self.deps_cpp_info["jasper"].rootpath if self.options.with_jasper else "no"))
        args.append("--with-openjpeg={}".format("yes" if self.options.with_openjpeg else "no"))
        args.append("--without-fgdb") # TODO: to implement when file-geodatabase-api lib available
        args.append("--without-ecw") # commercial library
        args.append("--without-kakadu") # commercial library
        args.extend(["--without-mrsid", "--without-jp2mrsid", "--without-mrsid_lidar"]) # commercial library
        args.append("--without-jp2lura") # commercial library
        args.append("--without-msg") # commercial library
        args.append("--without-oci") # TODO
        args.append("--with-gnm={}".format("yes" if self.options.with_gnm else "no"))
        args.append("--without-mysql") # TODO: which one to use?
        args.append("--without-ingres") # commercial library
        args.append("--with-xerces={}".format(self.deps_cpp_info["xerces-c"].rootpath if self.options.with_xerces else "no"))
        args.append("--with-expat={}".format(self.deps_cpp_info["expat"].rootpath if self.options.with_expat else "no"))
        args.append("--with-libkml={}".format(self.deps_cpp_info["libkml"].rootpath if self.options.with_libkml else "no"))
        args.append("--with-odbc={}".format(self.deps_cpp_info["odbc"].rootpath if self.options.with_odbc else "no"))
        args.append("--without-dods-root") # TODO: to implement when libdap lib available
        args.append("--with-curl={}".format("yes" if self.options.with_curl else "no"))
        args.append("--with-xml2={}".format("yes" if self.options.with_xml2 else "no"))
        args.append("--without-spatialite") # TODO: to implement when spatialite lib available
        args.append("--with-sqlite3={}".format(self.deps_cpp_info["sqlite3"].rootpath if self.options.get_safe("with_sqlite3") else "no"))
        args.append("--without-rasterlite2") # TODO: to implement when rasterlite2 lib available
        args.append("--with-pcre={}".format("yes" if self.options.get_safe("with_pcre") else "no"))
        args.append("--without-teigha") # commercial library
        args.append("--without-idb") # commercial library
        args.append("--without-sde") # commercial library
        args.append("--without-epsilon") # TODO: to implement when epsilon lib available
        args.append("--with-webp={}".format(self.deps_cpp_info["libwebp"].rootpath if self.options.with_webp else "no"))
        args.append("--with-geos={}".format("yes" if self.options.with_geos else "no"))
        args.append("--without-sfcgal") # TODO: to implement when sfcgal lib available
        args.append("--with-qhull={}".format("internal" if self.options.with_qhull else "no")) # TODO: use conan recipe when available instead of internal one
        args.append("--without-opencl") # TODO: to implement when opencl-headers available (and also OpenCL lib?)
        args.append("--without-freexl") # TODO: to implement when freexl lib available
        args.append("--with-libjson-c=yes") # jsonc-c (required !)
        if self.options.without_pam:
            args.append("--without-pam")
        if self.options.enable_pdf_plugin:
            args.append("--enable-pdf-plugin")
        args.append("--without-poppler") # TODO: to implement when poppler lib available
        args.append("--without-podofo") # TODO: to implement when podofo lib available
        args.append("--without-pdfium") # TODO: to implement when pdfium lib available
        args.append("--without-perl")
        args.append("--without-python")
        args.append("--without-java")
        args.append("--without-hdfs")
        if tools.Version(self.version) >= "3.0.0":
            args.append("--without-tiledb") # TODO: to implement when tiledb lib available
        args.append("--without-mdb")
        args.append("--without-rasdaman") # TODO: to implement when rasdaman lib available
        if tools.Version(self.version) >= "3.1.0":
            args.append("--without-rdb") # commercial library
        args.append("--without-armadillo") # TODO: to implement when armadillo lib available
        args.append("--without-cryptopp") # TODO: to implement when cryptopp lib available
        args.append("--with-crypto={}".format("yes" if self.options.with_crypto else "no"))
        args.append("--with-lerc={}".format("no" if self.options.without_lerc else "yes"))
        if self.options.with_null:
            args.append("--with-null")
        if self.options.get_safe("with_exr") is not None:
            args.append("--with-exr={}".format("yes" if self.options.with_exr else "no"))

        with tools.chdir(configure_dir):
            self._autotools.configure(args=args)
        return self._autotools

    def build(self):
        self._patch_sources()
        autotools = self._configure_autotools()
        with tools.chdir(os.path.join(self._source_subfolder, "gdal")):
            autotools.make()

    def _patch_sources(self):
        for patch in self.conan_data.get("patches", {}).get(self.version, []):
            tools.patch(**patch)
        # Remove embedded dependencies
        embedded_libs = [
            os.path.join("frmts", "gif", "giflib"),
            os.path.join("frmts", "jpeg", "libjpeg"),
            os.path.join("frmts", "png", "libpng"),
            os.path.join("frmts", "zlib"),
            os.path.join("ogr", "ogrsf_frmts", "geojson", "libjson"),
        ]
        if tools.Version(self.version) >= "3.1.0":
            embedded_libs.append(os.path.join("ogr", "ogrsf_frmts", "flatgeobuf", "flatbuffers"))
        for lib_subdir in embedded_libs:
            tools.rmdir(os.path.join(self._source_subfolder, "gdal", lib_subdir))

    def package(self):
        self.copy("LICENSE.TXT", dst="licenses", src=os.path.join(self._source_subfolder, "gdal"))
        autotools = self._configure_autotools()
        with tools.chdir(os.path.join(self._source_subfolder, "gdal")):
            autotools.install()
        tools.rmdir(os.path.join(self.package_folder, "share"))
        # tools.rmdir(os.path.join(self.package_folder, "lib", "gdalplugins"))
        tools.rmdir(os.path.join(self.package_folder, "lib", "pkgconfig"))
        for la_file in glob.glob(os.path.join(self.package_folder, "lib", "*.la")):
            os.remove(la_file)

    def package_info(self):
        self.cpp_info.names["cmake_find_package"] = "GDAL"
        self.cpp_info.names["cmake_find_package_multi"] = "GDAL"
        self.cpp_info.names["pkg_config"] = "gdal"
        self.cpp_info.libs = tools.collect_libs(self)
        if self.settings.os == "Linux":
            self.cpp_info.system_libs.extend(["m", "pthread"])
        if not self.options.shared and self._stdcpp_library:
            self.cpp_info.system_libs.append(self._stdcpp_library)

    @property
    def _stdcpp_library(self):
        libcxx = self.settings.get_safe("compiler.libcxx")
        if libcxx in ("libstdc++", "libstdc++11"):
            return "stdc++"
        elif libcxx in ("libc++",):
            return "c++"
        else:
            return False
