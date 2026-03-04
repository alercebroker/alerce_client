# Plot
def create_stamp_parameters(oid, survey, measurement_id, stamp_type, avro_url, call):
    if call == "plot":
        return (
            avro_url
            + f"?oid={oid}&measurement_id={measurement_id}&stamp_type={stamp_type}&file_format=png&survey_id={survey}"
        )
    elif call == "get":
        return (
            avro_url
            + f"?oid={oid}&measurement_id={measurement_id}&stamp_type={stamp_type}&file_format=fits&survey_id={survey}"
        )
