def message_template(
    first_word,
    morning_greeting,
    name,
    temp_real,
    temp_unit_long,
    temp_felt,
    temp_unit_short,
    cloudiness_percentage,
    condition,
    humidity_percentage,
    windspeed,
    speed_unit_long,
    assessment,
    russian_text,
) -> str:
    return (
        f"__**{first_word}**__\n"
        "\n"
        f"{morning_greeting} {name}, hope you have Exciting Day. (Just kidding your Stupid)\n"
        "\n"
        f"It is currently {temp_real} degrees {temp_unit_long} "
        f"(and it Feels like {temp_felt}{temp_unit_short}), "
        f"with cloudiness of {cloudiness_percentage}%. "
        f"In Fact, Outside it is {condition}, "
        f"with a humidity of {humidity_percentage}% "
        f"and windspeeds at {windspeed} {speed_unit_long}. "
        f"{assessment}\n"
        "\n"
        f"**{russian_text}**"
    )
