cmake_minimum_required(VERSION 3.22)

if(APPLE)
    set(CMAKE_OSX_DEPLOYMENT_TARGET "10.15" CACHE STRING "Minimum macOS deployment version" FORCE)
    set(CMAKE_OSX_ARCHITECTURES "arm64;x86_64" CACHE STRING "Build architectures for macOS" FORCE)
endif()

project(AnechoicMind VERSION 0.1.0)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

add_subdirectory(/Users/axiomrasa/dev/third-party/JUCE ${CMAKE_BINARY_DIR}/JUCE)

juce_add_plugin(AnechoicMind
    COMPANY_NAME "Axiom Rasa"
    BUNDLE_ID "com.axiomrasa.anechoicmind"
    PLUGIN_MANUFACTURER_CODE AxRs
    PLUGIN_CODE AnMn
    FORMATS VST3 AU Standalone
    PRODUCT_NAME "Anechoic Mind"
    IS_SYNTH FALSE
    NEEDS_MIDI_INPUT FALSE
    NEEDS_MIDI_OUTPUT FALSE
    IS_MIDI_EFFECT FALSE
    COPY_PLUGIN_AFTER_BUILD TRUE
)

juce_generate_juce_header(AnechoicMind)

target_sources(AnechoicMind PRIVATE
    dsp/anechoic_mind/FaustPluginProcessor.cpp
)

target_include_directories(AnechoicMind PRIVATE
    ${CMAKE_BINARY_DIR}/AnechoicMind_artefacts
)

target_compile_definitions(AnechoicMind PUBLIC
    JUCE_WEB_BROWSER=0
    JUCE_USE_CURL=0
    JUCE_VST3_CAN_REPLACE_VST2=0
    PlugIn=1
)

target_link_libraries(AnechoicMind PRIVATE
    juce::juce_audio_utils
    juce::juce_audio_processors
    juce::juce_gui_extra
    juce::juce_opengl
    PUBLIC
    juce::juce_recommended_config_flags
)
