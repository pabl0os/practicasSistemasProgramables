import machine, time

class HCSR04:
    def __init__(self, trigger_pin, echo_pin, echo_timeout_us=30000):
        self.trigger = machine.Pin(trigger_pin, machine.Pin.OUT)
        self.echo = machine.Pin(echo_pin, machine.Pin.IN)
        self.echo_timeout_us = echo_timeout_us

    def _send_pulse_and_wait(self):
        self.trigger.off()
        time.sleep_us(2)
        self.trigger.on()
        time.sleep_us(10)
        self.trigger.off()
        try:
            pulse_time = machine.time_pulse_us(self.echo, 1, self.echo_timeout_us)
            return pulse_time
        except OSError as ex:
            if ex.args[0] == 110:  # timeout
                raise OSError("Out of range")
            raise ex

    def distance_cm(self):
        pulse_time = self._send_pulse_and_wait()
        # velocidad del sonido = 340 m/s
        cms = (pulse_time / 2) / 29.1
        return cms

    def distance_mm(self):
        pulse_time = self._send_pulse_and_wait()
        mms = (pulse_time / 2) * 0.343
        return mms
