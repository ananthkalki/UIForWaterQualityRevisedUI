#include <linux/spi/spidev.h>
#include <fcntl.h>
#include <sys/ioctl.h>
#include <unistd.h>
#include <malloc.h>
#include <string.h>
#include <errno.h>
#include <stdint.h>
#include <wiringPi.h>
#include <stdio.h>
#include <ncurses.h>
#include <time.h>
#include <stdlib.h>
#include <sys/time.h>

#define tdc_enable_pin 1
#define osc_enable_pin 4
#define tdc1_interu_pin 25
#define tdc2_interu_pin 26
#define clockfrequency 8000000.0

float tMaxTDCIdle = 1;
bool NoActivityOnTDC = false;
int spi_fd;
int spi_mode = 0x00;
uint8_t spi_bpw = 8;//8=cs0 7=cs0
int spi_speed = 25000000;
uint16_t spi_delay = 0;
int spi_toggle_cs = 0;

double calib2periods = 10.0;
double clockperiod = 1.0/clockfrequency;

long getMicrotime();
int spi_open()
{
    spi_fd = open("/dev/spidev0.1",O_RDWR);
    if (spi_fd == -1)
    {
        printf("spi_open failed: %s\n",strerror(errno));
        return -1;
    }
    return 0;
}
int spi_close()
{
    close(spi_fd);
    return 0;
}
int spi_configure()
{
    int ret = ioctl(spi_fd, SPI_IOC_WR_MODE, &spi_mode);
    if (ret == -1)
    {
        printf("SPI_IOC_WR_MODE failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
    ret = ioctl(spi_fd, SPI_IOC_RD_MODE, &spi_mode);
    if (ret == -1)
    {
        printf("SPI_IOC_RD_MODE failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
    ret = ioctl(spi_fd, SPI_IOC_WR_BITS_PER_WORD, &spi_bpw);
    if (ret == -1)
    {
        printf("SPI_IOC_WR_BITS_PER_WORD failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
    ret = ioctl(spi_fd, SPI_IOC_RD_BITS_PER_WORD, &spi_bpw);
    if (ret == -1)
    {
        printf("SPI_IOC_RD_BITS_PER_WORD failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
    ret = ioctl(spi_fd, SPI_IOC_WR_MAX_SPEED_HZ, &spi_speed);
    if (ret == -1)
    {
        printf("SPI_IOC_WR_MAX_SPEED_HZ failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
    ret = ioctl(spi_fd, SPI_IOC_RD_MAX_SPEED_HZ, &spi_speed);
    if (ret == -1)
    {
        printf("SPI_IOC_RD_MAX_SPEED_HZ failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
    return 0;
}
int spi_txfr(uint8_t* data,int data_length)
{
    struct spi_ioc_transfer spi_xfr = {0};
    char txbuf[data_length];
    char rxbuf[data_length];
    memcpy(txbuf, data, data_length);
    memset(rxbuf, 0xff, data_length);
    spi_xfr.tx_buf        = (unsigned long)txbuf;
    spi_xfr.rx_buf        = (unsigned long)rxbuf;
    spi_xfr.len           = data_length;
    spi_xfr.speed_hz      = spi_speed;
    spi_xfr.delay_usecs   = spi_delay;
    spi_xfr.bits_per_word = spi_bpw;
    spi_xfr.cs_change     = spi_toggle_cs;
    spi_xfr.pad           = 0;
    int ret = ioctl(spi_fd, SPI_IOC_MESSAGE(1), &spi_xfr);
    if (ret < 0)
    {
        printf("SPI_IOC_MESSAGE failed: %s\n",strerror(errno));
        spi_close();
        return -1;
    }
	for(int i = 0; i<data_length;i++)
		data[i] = rxbuf[i];
    return 0;
}
/************************************************************
* TI TDC720x REGISTER SET ADDRESSES
************************************************************/

#define TI_TDC720x_CONFIG1_REG                         (0x00)                  //  
#define TI_TDC720x_CONFIG2_REG                         (0x01)                  //  
#define TI_TDC720x_INTRPT_STATUS_REG                   (0x02)                  //  
#define TI_TDC720x_INTRPT_MASK_REG                     (0x03)                  //  
#define TI_TDC720x_COARSE_COUNTER_OVH_REG              (0x04)                  //  
#define TI_TDC720x_COARSE_COUNTER_OVL_REG              (0x05)                  //  
#define TI_TDC720x_CLOCK_COUNTER_OVH_REG               (0x06)                  //  
#define TI_TDC720x_CLOCK_COUNTER_OVL_REG               (0x07)                  //  
#define TI_TDC720x_CLOCK_COUNTER_STOP_MASKH_REG        (0x08)                  //  
#define TI_TDC720x_CLOCK_COUNTER_STOP_MASKL_REG        (0x09)                  // 

#define TI_TDC720x_TIME1_REG                           (0x10)                  //  
#define TI_TDC720x_CLOCK_COUNT1_REG                    (0x11)                  //
#define TI_TDC720x_TIME2_REG                           (0x12)                  //  
#define TI_TDC720x_CLOCK_COUNT2_REG                    (0x13)                  // 
#define TI_TDC720x_TIME3_REG                           (0x14)                  //  
#define TI_TDC720x_CLOCK_COUNT3_REG                    (0x15)                  // 
#define TI_TDC720x_TIME4_REG                           (0x16)                  //  
#define TI_TDC720x_CLOCK_COUNT4_REG                    (0x17)                  //
#define TI_TDC720x_TIME5_REG                           (0x18)                  //  
#define TI_TDC720x_CLOCK_COUNT5_REG                    (0x19)                  // 
#define TI_TDC720x_TIME6_REG                           (0x1A)                  //
#define TI_TDC720x_CALIBRATION1_REG                    (0x1B)                  //
#define TI_TDC720x_CALIBRATION2_REG                    (0x1C)                  //

void tdc_send(uint8_t addr, uint8_t value) {
    uint8_t inst = 0x40 | (addr & 0x7F);
    uint8_t data[2];
    data[0] = inst;
    data[1] = value;
    spi_txfr(data,2);
}
uint8_t tdc_recv(uint8_t addr) {
	uint8_t inst = 0xBF & (addr & 0x7F);
	uint8_t data[2];
	data[0] = inst;
	data[1] = 0;
	spi_txfr(data,2);
	return data[1];
}
uint32_t tdc_long_recv(uint8_t addr)
{
	uint8_t inst = 0xBF & (addr & 0x7F);
    uint8_t data[3];
    data[0] = inst;
    data[1] = 0;
	data[2] = 0;
	data[3] = 0;
    spi_txfr(data,4);
    return data[1]<<16 | data[2]<<8 | data[3];
}
void tdc_init()
{
	if(wiringPiSetup() == -1)
	{
		printf("setup wiringPi failed !\n");
	}
	pinMode(tdc_enable_pin, OUTPUT);
	pinMode(osc_enable_pin, OUTPUT);
	pinMode(tdc2_interu_pin, INPUT);//Added to enable TDC2
	pinMode(tdc1_interu_pin, INPUT);
	digitalWrite(tdc_enable_pin, HIGH);
	digitalWrite(osc_enable_pin, HIGH);
	spi_open();
	spi_configure();
	printf("TI_TDC720x_CONFIG1_REG: %x\n",tdc_recv(TI_TDC720x_CONFIG1_REG));
	printf("TI_TDC720x_CONFIG2_REG: %x\n",tdc_recv(TI_TDC720x_CONFIG2_REG));
	tdc_send(TI_TDC720x_COARSE_COUNTER_OVH_REG,0x01);	
	tdc_send(TI_TDC720x_COARSE_COUNTER_OVL_REG,0x20);///0x01f = 100us

	printf("TI_TDC720x_COARSE_COUNTER_OVH_REG: %x\n",tdc_recv(TI_TDC720x_COARSE_COUNTER_OVH_REG));
	printf("TI_TDC720x_COARSE_COUNTER_OVL_REG: %x\n",tdc_recv(TI_TDC720x_COARSE_COUNTER_OVL_REG));
}
void tdc_deinit()
{
	spi_close();
}
double tdc_measure()
{
	tdc_send(TI_TDC720x_CONFIG1_REG,0x01);//Start Measurement
	//time_t tMeasStart=time(NULL);
	//struct timeval tval_before, tval_after, tval_result;
    //gettimeofday(&tval_before, NULL);
	//printf("Waiting for measurement\n");
	while(digitalRead(tdc2_interu_pin))//Waiting for TDC 2 interrupt to deassert
	{
	   // gettimeofday(&tval_after, NULL); 	
       // timersub(&tval_after, &tval_before, &tval_result);
       // if (tval_result.tv_usec>200)//Detects if the TDC is idle for more than 200 microseconds (arrived by experimental testing) and breaks out
	   // {
		   // printf("TDC is idle fot too long!\n");
		   // NoActivityOnTDC=true;
		   // break;
	   // }
	}//;Wait for start and stop
	//printf("Measurement done\n");
	double calib1 = (double)tdc_long_recv(TI_TDC720x_CALIBRATION1_REG);
	double calib2 = (double)tdc_long_recv(TI_TDC720x_CALIBRATION2_REG);
	//The following three lines of code are being moved out as global steps to reduce redundant delay.
	//double calib2periods = 10.0;
	//double clockfrequency = 8000000.0;
	//double clockperiod = 1.0 / clockfrequency;
	double tdctime = (double)(tdc_long_recv(TI_TDC720x_TIME1_REG) & 0x7FFFFF);//Get time counter value
	double calcount = (calib2 - calib1) / (calib2periods - 1.0);
	double normLSB = (clockperiod / calcount)*1000000000;
	double TOF = tdctime * normLSB;
	return TOF;
}
void tdc_store(double value)
{
	FILE *fptr = fopen("/home/pi/samplesdir/export.csv","a");
	if(fptr == NULL)
		printf("File open failed: %s",strerror(errno));
	fprintf(fptr,"%f\n",value); //fprintf(fptr,"%lu,%f\n",getMicrotime(),value);
	fclose(fptr);
}
void main()
{
	// while(1)
	// {
	// printf("%lu\n",getMicrotime());
    //      sleep(1);
  
    // }
	uint32_t counts = 0;
	int a;
	int start_time, stop_time=0, Time_taken=0;
	int ExpDone = 0;
	// SetTimeMin = 5;//Set the time for which data will be acquired in seconds
	int SetTime=2;
	tdc_init();
	// WINDOW *win = initscr();
	// nodelay(win,TRUE);
	// noecho();
	
	//scanf("%f",&SetTimeMin);
	//printf("%f\n",SetTimeMin);
	//SetTime = SetTimeMin*60.0;

	time_t time_start = time(NULL);

	printf("%d\n",SetTime);
	FILE *fptr = fopen("/home/pi/samplesdir/export.csv","a");
	if(fptr == NULL)
		printf("File open failed: %s",strerror(errno));
	fprintf(fptr,"tof\n");
	printf("OVER HERE");
	//fprintf(fptr,"Time (us),tof\n");
	fclose(fptr);
	// start_time = time(NULL);
	// printf("Start time =  %d\n",time(NULL));

	while(1)
	{
		int ch = getch();
		if(time(NULL)-time_start >=SetTime)
		{
			stop_time=time(NULL);
			Time_taken=stop_time-start_time;
			FILE *fptr = fopen("/home/pi/samplesdir/Report.csv","w");
			if(fptr == NULL)
				printf("File open failed: %s",strerror(errno));
			//fprintf(fptr,"%d\n",Time_taken);
			fclose(fptr);
			//printf("Time taken (min) = %d\n",Time_taken);
     		break;
		}
		// if(counts>=390200)
		// {
		// 	stop_time=time(NULL);
		// 	Time_taken=stop_time-start_time;
		// 	FILE *fptr = fopen("/home/pi/samplesdir/Report.csv","w");
		// 	if(fptr == NULL)
		// 		printf("File open failed: %s",strerror(errno));
		// 	fprintf(fptr,"%d\n",Time_taken);
		// 	fclose(fptr);
		// 	printf("Time taken (min) = %d\n",Time_taken);
     	// 	break;
		// }
		//printf("Calling TDC measure\n");
		double tdcval = tdc_measure();
		//printf("TDC no activity: %b\n",NoActivityOnTDC);
		// if(NoActivityOnTDC==true)
			// break;
		// NoActivityOnTDC = false;
		//printf("TDC measure done\n");
		if(tdcval<=100.00)
		{
			tdc_store(tdcval);
			counts++;
		}
	}
}

long getMicrotime(){
	struct timeval currentTime;
	gettimeofday(&currentTime, NULL);
	return currentTime.tv_sec * (int)1e6 + currentTime.tv_usec;
}
