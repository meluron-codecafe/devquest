#include <iostream>
#include <SFML/Audio.hpp>

int main() {
    sf::SoundBuffer buffer;
    if (!buffer.loadFromFile("/Users/ankit/Documents/meluron-codecafe/DevQuest/data/songs/song-1.mp3")) {
        std::cout << "Failed to load audio file\n";
        return -1;
    }

    const short* samples = buffer.getSamples();
    std::size_t sampleCount = buffer.getSampleCount();

    std::cout << "Total samples: " << sampleCount << "\n";
    std::cout << "Channels: " << buffer.getChannelCount() << "\n";
    std::cout << "Sample rate: " << buffer.getSampleRate() << " Hz\n";

    for (std::size_t i = 0; i < 10 && i < sampleCount; i++) {
        std::cout << samples[i] << " ";
    }
    std::cout << "\n";

    return 0;
}
