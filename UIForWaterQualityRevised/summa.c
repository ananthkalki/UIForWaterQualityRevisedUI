#include <iostream>
#include <chrono>
#include <ctime>

int main() {
    // Get the current system time
    auto currentTime = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());

    // Convert the time to a string
    char timeString[100];
    std::strftime(timeString, sizeof(timeString), "%Y-%m-%d %H:%M:%S", std::localtime(&currentTime));

    // Print the current time
    std::cout << "Current Time: " << timeString << std::endl;

    return 0;
}
