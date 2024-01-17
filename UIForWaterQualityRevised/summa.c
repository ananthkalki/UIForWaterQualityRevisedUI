#include <iostream>
#include <chrono>
#include <ctime>

#define tdc_enable_pin 1 ///GPIO1 ->pin 12
#define osc_enable_pin 4 ///GPIO4 ->pin 16
#define tdc1_interu_pin 25///GPIO25 ->pin 37
#define tdc2_interu_pin 26///GPIO26 ->pin 32

// ///////GPIO program define start ////////////////
#define BCM2708_PERI_BASE       0x3f000000
#define GPIO_BASE               (BCM2708_PERI_BASE + 0x200000)	// GPIO controller 

#define BLOCK_SIZE 		(4*1024)

#define INP_GPIO(g)   *(gpio.addr + ((g)/10)) &= ~(7<<(((g)%10)*3))
#define OUT_GPIO(g)   *(gpio.addr + ((g)/10)) |=  (1<<(((g)%10)*3))
 
#define GPIO_SET  *(gpio.addr + 7)  // sets   bits which are 1 ignores bits which are 0
#define GPIO_CLR  *(gpio.addr + 10) // clears bits which are 1 ignores bits which are 0
 
#define GPIO_READ(g)  *(gpio.addr + 13) &= (1<<(g))
// ////////GPIO program define end/////////////////////
struct bcm2835_peripheral {
    unsigned long addr_p;
    int mem_fd;
    void *map;
    volatile unsigned int *addr;
};
struct bcm2835_peripheral gpio = {GPIO_BASE};
#define GPIO_READ(g)  *(gpio.addr + 13) &= (1<<(g))

int main() {
    // Get the current system time
    auto currentTime = std::chrono::system_clock::to_time_t(std::chrono::system_clock::now());

    // Convert the time to a string
    char timeString[100];
    std::strftime(timeString, sizeof(timeString), "%Y-%m-%d %H:%M:%S", std::localtime(&currentTime));

    // Print the current time
    std::cout << "Current Time: "<<GPIO_READ(tdc2_interu_pin) << std::endl;

    return 0;
}
