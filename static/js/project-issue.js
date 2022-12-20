$('.submit-issue').click(function (e) {

    e.preventDefault();

    console.log("issue submitted");
    let issue_msg = document.getElementById('form-issue').value;
    document.getElementById('form-issue').value = '';
    let coord = document.getElementById('location-hidden').value;
    document.getElementById('location-hidden').value=''

    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    mydata = {
        issue_msg: issue_msg,
        coord: coord,
        csrfmiddlewaretoken: csrf_token,
    }

    $.ajax(
        {
            url: "issue/",
            method: 'POST',
            data: mydata,
            success: function (data) {

                console.log("issue submitted successfully");
                console.log(data);

            }
        }
    )

})
