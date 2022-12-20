$('.submit-rating').click(function (e) {

    e.preventDefault();
    console.log('rating trying to submit')


    let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    let rating = $("input[type='radio'][name='rating']:checked").val()
    let project_id = document.getElementById('location-hidden').value;
    document.getElementById('location-hidden').value = ''

    mydata = {
        // feedback_msg: feedback_msg,
        csrfmiddlewaretoken: csrf_token,
        rating: rating,
        project_id: project_id
    }
    console.log(mydata);
    // console.log(mydata);
    $.ajax(
        {
            url: "add-rating/",
            method: 'POST',
            data: mydata,
            success: function (data) {

                console.log(data)

                if (data.status == '1') {
                    console.log('rating submitted')
                    document.getElementById('toast-msg-body').innerText = 'Rating submitted successfully'
                    $("#success-toast").toast("show");
                }
                else{
                    document.getElementById('toast-msg-body-failure').innerText = 'Rating not submitted'
                    $("#failure-toast").toast("show");
                }

            }
        }
    )


})

// $.ajax(
//         {
//             url: "add-rating/",
//             method: 'POST',
//             data: mydata,
//             success: function (data) {
//
//                 console.log("rating submitted successfully");
//                 console.log(data);
//
//             }
//         }
//     )