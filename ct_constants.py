ct1_solenoid_map = {
    0: 8,
    1: 6,
    2: 12,
    3: 4,
    4: 3,
    5: 2,
    6: 1,
    7: 13,
    8: 0,
    9: 11,
    10: 15,
    11: 5,
    12: 14,
}

ct1_led_map = {
        0: None,
        1: 0,
        2: 1,
        3: 2,
        4: 3,
        5: 4,
        6: 5,
        7: 6,
        8: 15,
        9: 14,
        10: 13,
        11: 12,
        12: 11,
        }

MAJOR_ARP = [1, 3, 5, 8]

SOLENOID_MUX_ADDR = 0x20
LED_MUX_ADDR = 0x24
CT_BUTTON_GPIO_PIN = 21
SOLENOID_ON_TIME = 0.1
POLLING_INTERVAL = 0.01
