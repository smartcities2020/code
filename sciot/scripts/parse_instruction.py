#!/usr/bin/python
import sys
from pub import send_instruction


def parse_instruction(text):
    instruction = text[text.find('step')+4: text.find('time spent')]

    instruction_steps = []

    for row in instruction.split('\n'):
        parts = row.strip().split(':')
        if len(parts) == 1:
            continue
        step = int(parts[0])
        rest = ' '.join(parts[1:])
        parts = [part.strip() for part in rest.split(' ') if part !='']
        command = parts[0]
        sensors = parts[1:]
        instruction_steps.append({
            'step': step,
            'command': command,
            'sensors': sensors})

        for sensor in sensors:
            send_instruction(sensor, command)

if __name__ == '__main__':
    parse_instruction(sys.stdin.read())
