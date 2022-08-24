from random import choice


def fix(string: str) -> str:
    return "".join(string.lower().split()).removeprefix("to")


reasons = list(
    enumerate(
        (s, fix(s))
        for s in (
            "It's required",
            "The USA is a democracy",
            "gov & its decisions have a large impact",
            "government is complex",
            "Know your rights",
            "it is your duty",
            "Improve academic skills",
            "to inspire and appreciate democracy",
        )
    )
)

for i, (reason, _) in reasons:
    print(f"#{i+1}: {reason}")
print()

try:
    while True:
        i, (correct, match) = choice(reasons)
        text = fix(input(f"#{i+1}: "))
        if text == match:
            print("correct!")
        else:
            print(f"wrong: {correct}")
        print()
except KeyboardInterrupt:
    print()
    print("Goodbye!")
