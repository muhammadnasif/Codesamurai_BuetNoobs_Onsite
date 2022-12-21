


window.addEventListener('load', function (e){
  console.log("Proposed Called");
})
function ProposalEdit(){
  console.log("Proposal Edit Called");
  let core = document.getElementById('core_id').value;
  document.getElementById('core_id').value=null;
  console.log(core);
}


// $('.btn-proposal-edit').click(function(e){

//       console.log("button pressed .... shala bolod")
//       let x = $(this).attr('data-core-id');
//       console.log(x)
//     let csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
//     mydata = {
//         core_id: x,
//         csrfmiddlewaretoken: csrf_token,
//     }
//   $.ajax(
//         {
//             url: "update-proposal/",
//             method: 'POST',
//             data: mydata,
//             success: function (data) {

//                 console.log("issue submitted successfully");
//                 console.log(data);

//             }
//         }
//     )

// })
