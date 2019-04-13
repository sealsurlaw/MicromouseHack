import RPi.GPIO as GPIO
import time
import signal
import sys

class Driver:
    def __init__(self):
        self.IN1 = 5
        self.IN2 = 3
        self.IN3 = 13
        self.IN4 = 11

        self.PWM1 = 32
        self.PWM2 = 33

        self.SEN1TRIG = 8
        self.SEN1ECHO = 10

        self.SEN2TRIG = 16
        self.SEN2ECHO = 18

        self.SEN3TRIG = 21
        self.SEN3ECHO = 23

        GPIO.setmode( GPIO.BOARD )
    
        GPIO.setup( self.IN1, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.IN2, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.IN3, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.IN4, GPIO.OUT, initial=GPIO.LOW )

        GPIO.setup( self.PWM1, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.PWM2, GPIO.OUT, initial=GPIO.LOW )

        self.p1 = GPIO.PWM( self.PWM1, 2000 )
        self.p2 = GPIO.PWM( self.PWM2, 2000 )

        self.p1.start(0)
        self.p2.start(0)

        GPIO.setup( self.SEN1TRIG, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.SEN1ECHO, GPIO.IN )

        GPIO.setup( self.SEN2TRIG, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.SEN2ECHO, GPIO.IN )

        GPIO.setup( self.SEN3TRIG, GPIO.OUT, initial=GPIO.LOW )
        GPIO.setup( self.SEN3ECHO, GPIO.IN )


    # Destructor
    def __del__(self):
        GPIO.cleanup()


    def changeSpeed(self, speed, side='both'):
        if side == 'left':
            self.p1.ChangeDutyCycle( speed )
        if side == 'right':
            self.p2.ChangeDutyCycle( speed )
        else:
            self.p1.ChangeDutyCycle( speed )
            self.p2.ChangeDutyCycle( speed )


    def forward(self, speed=50):
        GPIO.output( self.IN1, GPIO.LOW )
        GPIO.output( self.IN2, GPIO.HIGH )
        GPIO.output( self.IN3, GPIO.LOW )
        GPIO.output( self.IN4, GPIO.HIGH )

        self.p1.ChangeDutyCycle( speed )
        self.p2.ChangeDutyCycle( speed )


    def backward(self, speed=50, frequency=500):
        GPIO.output( self.IN1, GPIO.HIGH )
        GPIO.output( self.IN2, GPIO.LOW )
        GPIO.output( self.IN3, GPIO.HIGH )
        GPIO.output( self.IN4, GPIO.LOW )

        self.p1.ChangeDutyCycle( speed )
        self.p2.ChangeDutyCycle( speed )


    def left(self, duration=0.2, speed=50, frequency=500):
        self.p1.stop()
        self.p2.stop()

        # Left wheel
        GPIO.output( self.IN1, GPIO.LOW )
        GPIO.output( self.IN2, GPIO.HIGH )
        #Right wheel
        GPIO.output( self.IN3, GPIO.HIGH )
        GPIO.output( self.IN4, GPIO.LOW )

        self.p1 = GPIO.PWM( self.PWM1, frequency )
        self.p2 = GPIO.PWM( self.PWM2, frequency )

        self.p1.start( speed )
        self.p2.start( speed )

        time.sleep( duration )

        self.stop()
        

    def right(self, duration=0.2, speed=50, frequency=500):
        self.p1.stop()
        self.p2.stop()

        # Left wheel
        GPIO.output( self.IN1, GPIO.HIGH )
        GPIO.output( self.IN2, GPIO.LOW )
        #Right wheel
        GPIO.output( self.IN3, GPIO.LOW )
        GPIO.output( self.IN4, GPIO.HIGH )

        self.p1 = GPIO.PWM( self.PWM1, frequency )
        self.p2 = GPIO.PWM( self.PWM2, frequency )

        self.p1.start( speed-3 )
        self.p2.start( speed )

        time.sleep( duration )

        #self.stop()
        self.p1.stop()
        self.p2.stop()


    def stop(self):
        self.p1.stop()
        self.p2.stop()

    def pingIndiv(self, trig, echo):
        # Ping left
        GPIO.output( trig, GPIO.HIGH )
        # After some time, stop pinging
        time.sleep(0.00001)
        GPIO.output( trig, GPIO.LOW )

        startTime = time.time()
        stopTime = time.time()

        # Save start time
        while GPIO.input( echo ) == GPIO.LOW:
            startTime = time.time()

        # Save time of arrival
        while GPIO.input( echo ) == GPIO.HIGH:
            stopTime = time.time()

        timeElapsed = stopTime - startTime

        # Distance in centimeters
        distance = (timeElapsed * 34300) / 2

        return distance

    def ping(self):
        sen1 = self.pingIndiv( self.SEN1TRIG, self.SEN1ECHO )
        sen2 = self.pingIndiv( self.SEN2TRIG, self.SEN2ECHO )
        sen3 = self.pingIndiv( self.SEN3TRIG, self.SEN3ECHO )

        return sen1, sen2, sen3

