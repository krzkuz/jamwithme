// var form = document.getElementById('form')

// function Alert(){
//     alert(form.value);
// }

// form.addEventListener('submit', (e)=>{
//     if(e.keyCode === 13){
//         Alert();
//     }
// });


// function HandleSubmission()
// {
//    var form = document.getElementById("form-id");
//    // Replace with code for handling submission.
// }

// function CheckForEnterClick(e)
// {
//    e = e || window.event;
//    if( e.keyCode == 13 || e.which == 13 ) { HandleSubmission(); }
// }

// var addEventHandler = function(element,eventType,functionRef)
// {
//     if( element == null || typeof(element) == 'undefined' ) { return; }
//     if( element.addEventListener ) { element.addEventListener(eventType,functionRef,false); }
//     else if( element.attachEvent ) { element.attachEvent("on"+eventType,functionRef); }
//     else { element["on"+eventType] = functionRef; }
// };

// addEventHandler(window,"keydown",CheckForEnterClick);

// function sendRequest(){
//     console.log("Hello");
//     $.ajax({
//         url:'{% url "get-new-notifications" %}',
//         type:'json',
//         method:'GET',
//       data: {
//         action: 'get'
//       },
//       success: function(result){
//           $('#notification-count').text(result.length); //insert text of test.php into your div
//           setTimeout(function(){
//               sendRequest(); //this will send request again and again;
//           }, 1000);
//       }
//       });
//   }