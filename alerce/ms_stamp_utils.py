
# Plot
def create_stamp_parameters(oid, survey, measurement_id, stamp_type, avro_url, call):
    if call == 'plot':
        return avro_url + f"?oid={oid}&measurement_id={measurement_id}&stamp_type={stamp_type}&file_format=png&survey_id={survey}"
    elif call == 'get':
        print(avro_url + f"?oid={oid}&measurement_id={measurement_id}&stamp_type={stamp_type}&file_format=fit&survey_id={survey}")
        return avro_url + f"?oid={oid}&measurement_id={measurement_id}&stamp_type={stamp_type}&file_format=fit&survey_id={survey}"




def create_html_stamp_display(oid, measurement_id, science, template, difference):
    return f"""
        <div>ZTF oid:{oid}, measurement_id:{measurement_id} </div>
        <div>&emsp;&emsp;&emsp;&emsp;&emsp;
        Science
        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        Template
        &emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;
        Difference
        <div class="container">
            <div style="float:left;width:20%"><img src="{science}"></div>
            <div style="float:left;width:20%"><img src="{template}"></div>
            <div style="float:left;width:20%"><img src="{difference}"></div>
        </div>
        """