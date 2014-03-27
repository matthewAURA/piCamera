cmake_minimum_required(VERSION 2.8)
project( lineTrack )
find_package( OpenCV REQUIRED )
include_directories( ${OpenCV_INCLUDE_DIRS} lib/)
add_executable( lineTrack lineTrack.cpp lib/BallFinder.cpp lib/BlobObject.cpp lib/GUI.cpp lib/ImageProccessor.cpp lib/LineFinder.cpp lib/LineObject.cpp )
add_executable( linefind linefind.cpp lib/BallFinder.cpp lib/BlobObject.cpp lib/GUI.cpp lib/ImageProccessor.cpp lib/LineFinder.cpp lib/LineObject.cpp )

target_link_libraries( lineTrack ${OpenCV_LIBS} )
target_link_libraries( linefind ${OpenCV_LIBS} )
