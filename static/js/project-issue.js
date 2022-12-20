$('.submit-issue').click(function (e) {

    e.preventDefault();

    console.log("issue submitted");
    let feedback_msg = document.getElementById('form-issue').value;
    document.getElementById('form-issue').value = '';
    let project_id = document.getElementById('location-hidden').value;
    document.getElementById('location-hidden').value = ''

    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();

    mydata = {
        feedback_msg: feedback_msg,
        csrfmiddlewaretoken: csrf_token,
        project_id: project_id
    }

    console.log(mydata);

    $.ajax(
        {
            url: "post_feedback/",
            method: 'POST',
            data: mydata,
            success: function (data) {
                console.log(data)
                if (data.status == '1') {
                    document.getElementById('toast-msg-body').innerText = 'Feedback submitted successfully'
                    $("#success-toast").toast("show");
                }

            }
        }
    )
})

