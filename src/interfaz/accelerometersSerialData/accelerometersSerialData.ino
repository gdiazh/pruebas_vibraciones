/************************************************************
MPU9250_Basic
 Basic example sketch for MPU-9250 DMP Arduino Library 
Jim Lindblom @ SparkFun Electronics
original creation date: November 23, 2016
https://github.com/sparkfun/SparkFun_MPU9250_DMP_Arduino_Library

This example sketch demonstrates how to initialize the 
MPU-9250, and stream its sensor outputs to a serial monitor.

Development environment specifics:
Arduino IDE 1.6.12
SparkFun 9DoF Razor IMU M0

Supported Platforms:
- ATSAMD21 (Arduino Zero, SparkFun SAMD21 Breakouts)
*************************************************************/
#include <SparkFunMPU9250-DMP.h>

#define SerialPort SerialUSB

MPU9250_DMP imu;
MPU9250_DMP imu2;

// communication
#define PACKET_SZ 32
typedef struct{
    float a1x;
    float a1y;
    float a1z;
    float a2x;
    float a2y;
    float a2z;
    float time;
    uint8_t tail1;
    uint8_t tail2;
    uint8_t tail3;
    uint8_t checksum;
}Data;

Data data;

typedef struct{
    uint16_t var;
    uint8_t var2;
    uint8_t checksum;
}Data2;

Data2 data2;

void setup() 
{
  SerialPort.begin(115200);

  // Call imu.begin() to verify communication with and
  // initialize the MPU-9250 to it's default values.
  // Most functions return an error code - INV_SUCCESS (0)
  // indicates the IMU was present and successfully set up
  imu.getI2cAddr(0x68);
  if (imu.begin() != INV_SUCCESS)
  {
    while (1)
    {
      SerialPort.println("Unable to communicate with MPU-9250");
      SerialPort.println("Check connections, and try again.");
      SerialPort.println();
      delay(5000);
    }
  }
  imu2.getI2cAddr(0x69);
  if (imu2.begin() != INV_SUCCESS)
  {
    while (1)
    {
      SerialPort.println("Unable to communicate with MPU-9250 2");
      SerialPort.println("Check connections, and try again.");
      SerialPort.println();
      delay(5000);
    }
  }

  // Use setSensors to turn on or off MPU-9250 sensors.
  // Any of the following defines can be combined:
  // INV_XYZ_GYRO, INV_XYZ_ACCEL, INV_XYZ_COMPASS,
  // INV_X_GYRO, INV_Y_GYRO, or INV_Z_GYRO
  // Enable all sensors:
  imu.getI2cAddr(0x68);
  imu.setSensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);

  // Use setGyroFSR() and setAccelFSR() to configure the
  // gyroscope and accelerometer full scale ranges.
  // Gyro options are +/- 250, 500, 1000, or 2000 dps
  imu.setGyroFSR(2000); // Set gyro to 2000 dps
  // Accel options are +/- 2, 4, 8, or 16 g
  imu.setAccelFSR(16); // Set accel to +/-16g
  // Note: the MPU-9250's magnetometer FSR is set at 
  // +/- 4912 uT (micro-tesla's)

  // setLPF() can be used to set the digital low-pass filter
  // of the accelerometer and gyroscope.
  // Can be any of the following: 188, 98, 42, 20, 10, 5
  // (values are in Hz).
  imu.setLPF(5); // Set LPF corner frequency to 5Hz
  // The sample rate of the accel/gyro can be set using
  // setSampleRate. Acceptable values range from 4Hz to 1kHz
  imu.setSampleRate(1000); // Set sample rate to 1KHz

  // Likewise, the compass (magnetometer) sample rate can be
  // set using the setCompassSampleRate() function.
  // This value can range between: 1-100Hz
  imu.setCompassSampleRate(10); // Set mag rate to 10Hz


  imu2.getI2cAddr(0x69);
  imu2.setSensors(INV_XYZ_GYRO | INV_XYZ_ACCEL | INV_XYZ_COMPASS);
  imu2.setGyroFSR(2000); // Set gyro to 2000 dps
  imu2.setAccelFSR(16); // Set accel to +/-16g
  imu2.setLPF(5); // Set LPF corner frequency to 5Hz
  imu2.setSampleRate(1000); // Set sample rate to 1KHz
  imu2.setCompassSampleRate(10); // Set mag rate to 10Hz

}

void loop() 
{
  // dataReady() checks to see if new accel/gyro data
  // is available. It will return a boolean true or false
  // (New magnetometer data cannot be checked, as the library
  //  runs that sensor in single-conversion mode.)
  if ( imu.dataReady() )
  {
    // Call update() to update the imu objects sensor data.
    // You can specify which sensors to update by combining
    // UPDATE_ACCEL, UPDATE_GYRO, UPDATE_COMPASS, and/or
    // UPDATE_TEMPERATURE.
    // (The update function defaults to accel, gyro, compass,
    //  so you don't have to specify these values.)
    imu.getI2cAddr(0x68);
    imu.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
    // printIMUData();
  }

  if ( imu2.dataReady() )
  {
    // Call update() to update the imu objects sensor data.
    // You can specify which sensors to update by combining
    // UPDATE_ACCEL, UPDATE_GYRO, UPDATE_COMPASS, and/or
    // UPDATE_TEMPERATURE.
    // (The update function defaults to accel, gyro, compass,
    //  so you don't have to specify these values.)
    imu2.getI2cAddr(0x69);
    imu2.update(UPDATE_ACCEL | UPDATE_GYRO | UPDATE_COMPASS);
    // printIMU2Data();
  }
  // printIMUsData();

  // send data
  imu.getI2cAddr(0x68);
  data.a1x = imu.calcAccel(imu.ax);
  data.a1y = imu.calcAccel(imu.ay);
  data.a1z = imu.calcAccel(imu.az);
  imu2.getI2cAddr(0x69);
  data.a2x = imu2.calcAccel(imu2.ax);
  data.a2y = imu2.calcAccel(imu2.ay);
  data.a2z = imu2.calcAccel(imu2.az);
  data.time = imu.time;
  data.tail1 = 255;
  data.tail2 = 254;
  data.tail3 = 253;
  // data.a1x = 13.45;
  // data.a1y = -12.87;
  // data.a1z = 0.31;
  // data.a2x = 1.4;
  // data.a2y = 1.99;
  // data.a2z = -0.98;
  // data.time = 3.24;
  // data.tail1 = 74;
  // data.tail2 = 63;
  // data.tail3 = 21;
  data.checksum = checksum((uint8_t*)&data, sizeof(data));

  // data2.var = 398;
  // data2.var2 = 124;
  // data2.checksum = checksum((uint8_t*)&data2, sizeof(data2));
  // SerialPort.println(data2.checksum);

  SerialPort.write((uint8_t*)&data, sizeof(data));
}

void printIMUData(void)
{  
  // After calling update() the ax, ay, az, gx, gy, gz, mx,
  // my, mz, time, and/or temerature class variables are all
  // updated. Access them by placing the object. in front:

  // Use the calcAccel, calcGyro, and calcMag functions to
  // convert the raw sensor readings (signed 16-bit values)
  // to their respective units.
  float accelX = imu.calcAccel(imu.ax);
  float accelY = imu.calcAccel(imu.ay);
  float accelZ = imu.calcAccel(imu.az);
  float gyroX = imu.calcGyro(imu.gx);
  float gyroY = imu.calcGyro(imu.gy);
  float gyroZ = imu.calcGyro(imu.gz);
  float magX = imu.calcMag(imu.mx);
  float magY = imu.calcMag(imu.my);
  float magZ = imu.calcMag(imu.mz);
  
  SerialPort.println("Accel: " + String(accelX) + ", " +
              String(accelY) + ", " + String(accelZ) + " g");
  SerialPort.println("Gyro: " + String(gyroX) + ", " +
              String(gyroY) + ", " + String(gyroZ) + " dps");
  SerialPort.println("Mag: " + String(magX) + ", " +
              String(magY) + ", " + String(magZ) + " uT");
  SerialPort.println("Time: " + String(imu.time) + " ms");
  SerialPort.println();
}

void printIMU2Data(void)
{  
  // After calling update() the ax, ay, az, gx, gy, gz, mx,
  // my, mz, time, and/or temerature class variables are all
  // updated. Access them by placing the object. in front:

  // Use the calcAccel, calcGyro, and calcMag functions to
  // convert the raw sensor readings (signed 16-bit values)
  // to their respective units.
  float accelX_2 = imu2.calcAccel(imu2.ax);
  float accelY_2 = imu2.calcAccel(imu2.ay);
  float accelZ_2 = imu2.calcAccel(imu2.az);
  float gyroX_2 = imu2.calcGyro(imu2.gx);
  float gyroY_2 = imu2.calcGyro(imu2.gy);
  float gyroZ_2 = imu2.calcGyro(imu2.gz);
  float magX_2 = imu2.calcMag(imu2.mx);
  float magY_2 = imu2.calcMag(imu2.my);
  float magZ_2 = imu2.calcMag(imu2.mz);
  
  SerialPort.println("\t\t\t\t\t\tAccel2: " + String(accelX_2) + ", " +
              String(accelY_2) + ", " + String(accelZ_2) + " g");
  SerialPort.println("\t\t\t\t\t\tGyro2: " + String(gyroX_2) + ", " +
              String(gyroY_2) + ", " + String(gyroZ_2) + " dps");
  SerialPort.println("\t\t\t\t\t\tMag2: " + String(magX_2) + ", " +
              String(magY_2) + ", " + String(magZ_2) + " uT");
  SerialPort.println("\t\t\t\t\t\tTime: " + String(imu.time) + " ms");
  SerialPort.println();
}


void printIMUsData(void)
{  
  // After calling update() the ax, ay, az, gx, gy, gz, mx,
  // my, mz, time, and/or temerature class variables are all
  // updated. Access them by placing the object. in front:

  // Use the calcAccel, calcGyro, and calcMag functions to
  // convert the raw sensor readings (signed 16-bit values)
  // to their respective units.
  float accelX = imu.calcAccel(imu.ax);
  float accelY = imu.calcAccel(imu.ay);
  float accelZ = imu.calcAccel(imu.az);
  float gyroX = imu.calcGyro(imu.gx);
  float gyroY = imu.calcGyro(imu.gy);
  float gyroZ = imu.calcGyro(imu.gz);
  float magX = imu.calcMag(imu.mx);
  float magY = imu.calcMag(imu.my);
  float magZ = imu.calcMag(imu.mz);

  float accelX_2 = imu2.calcAccel(imu2.ax);
  float accelY_2 = imu2.calcAccel(imu2.ay);
  float accelZ_2 = imu2.calcAccel(imu2.az);
  float gyroX_2 = imu2.calcGyro(imu2.gx);
  float gyroY_2 = imu2.calcGyro(imu2.gy);
  float gyroZ_2 = imu2.calcGyro(imu2.gz);
  float magX_2 = imu2.calcMag(imu2.mx);
  float magY_2 = imu2.calcMag(imu2.my);
  float magZ_2 = imu2.calcMag(imu2.mz);

  
  SerialPort.println("Accel: " + String(accelX) + ", " +
              String(accelY) + ", " + String(accelZ) + " g");
  SerialPort.println("Accel2: " + String(accelX_2) + ", " +
              String(accelY_2) + ", " + String(accelZ_2) + " g");
  

  SerialPort.println("Gyro: " + String(gyroX) + ", " +
              String(gyroY) + ", " + String(gyroZ) + " dps");
  SerialPort.println("Gyro2: " + String(gyroX_2) + ", " +
              String(gyroY_2) + ", " + String(gyroZ_2) + " dps");
  

  SerialPort.println("Mag: " + String(magX) + ", " +
              String(magY) + ", " + String(magZ) + " uT");
  SerialPort.println("Mag2: " + String(magX_2) + ", " +
              String(magY_2) + ", " + String(magZ_2) + " uT");
  

  SerialPort.println("Time: " + String(imu.time) + " ms");
  
  SerialPort.println();
}

uint8_t checksum(uint8_t *packet, uint8_t n)
{
    uint32_t sum = 0;
    // SerialPort.println(n);
    for (int j=0;j<n-1;j++) sum += packet[j];
    return sum & 0x00FF;
}