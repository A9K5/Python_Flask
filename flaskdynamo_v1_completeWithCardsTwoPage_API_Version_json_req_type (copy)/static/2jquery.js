$(document).ready(function(){
    var table =  $('#myTable');
//    var a = [{"play_id":"1","question1":"135","q1r":"1","question2":"138","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"6","amount":"1.7","bet_amount":"10","winning_amount":"20","no_of_players":"10"},{"play_id":"2","question1":"130","q1r":"1","question2":"","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"3","amount":"1.7","bet_amount":"10","winning_amount":"50","no_of_players":"5"},{"play_id":"3","question1":"114","q1r":"0","question2":"123","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"2","amount":"0.56","bet_amount":"2","winning_amount":"4","no_of_players":"13"},{"play_id":"4","question1":"102","q1r":"1","question2":"107","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"5","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"5","question1":"101","q1r":"0","question2":"106","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"0","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"6","question1":"135","q1r":"1","question2":"138","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"6","amount":"1.7","bet_amount":"10","winning_amount":"20","no_of_players":"10"},{"play_id":"7","question1":"130","q1r":"1","question2":"","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"3","amount":"1.7","bet_amount":"10","winning_amount":"50","no_of_players":"5"},{"play_id":"8","question1":"114","q1r":"0","question2":"123","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"2","amount":"0.56","bet_amount":"2","winning_amount":"4","no_of_players":"13"},{"play_id":"9","question1":"102","q1r":"1","question2":"107","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"5","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"10","question1":"101","q1r":"0","question2":"106","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"0","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"11","question1":"135","q1r":"1","question2":"138","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"6","amount":"1.7","bet_amount":"10","winning_amount":"20","no_of_players":"10"},{"play_id":"12","question1":"130","q1r":"1","question2":"","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"3","amount":"1.7","bet_amount":"10","winning_amount":"50","no_of_players":"5"},{"play_id":"13","question1":"114","q1r":"0","question2":"123","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"2","amount":"0.56","bet_amount":"2","winning_amount":"4","no_of_players":"13"},{"play_id":"14","question1":"102","q1r":"1","question2":"107","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"5","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"15","question1":"101","q1r":"0","question2":"106","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"0","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"16","question1":"101","q1r":"0","question2":"106","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"0","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"17","question1":"135","q1r":"1","question2":"138","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"6","amount":"1.7","bet_amount":"10","winning_amount":"20","no_of_players":"10"},{"play_id":"18","question1":"130","q1r":"1","question2":"","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"3","amount":"1.7","bet_amount":"10","winning_amount":"50","no_of_players":"5"},{"play_id":"19","question1":"114","q1r":"0","question2":"123","q2r":"1","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"2","amount":"0.56","bet_amount":"2","winning_amount":"4","no_of_players":"13"},{"play_id":"20","question1":"102","q1r":"1","question2":"107","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"5","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"},{"play_id":"21","question1":"101","q1r":"0","question2":"106","q2r":"0","question3":"","q3r":"0","question4":"","q4r":"0","total_point":"0","amount":"0.85","bet_amount":"3","winning_amount":"4","no_of_players":"15"}];
//    var c = [{'_id':'2018-06-26 11:14:22.122','NAME1':'qw','EMAIL':'qweeqw@s.com','ADDRESS':{'A1':['asdasda','asdasdasdasd','3546546546']},'ID':'47','CONTACTNO':'786567'},{'_id':'2018-06-26 15:00:08.009','NAME1':'Tarun','EMAIL':'asd@we.com','ADDRESS':{'A1':['asdasda','asdasdasdasd','3546546546']},'ID':'55','CONTACTNO':'123123123123'}];
   var b = document.getElementById("myText").value;
//    console.log(typeof(b));
  //  console.log(JSON.stringify(b));
  //  var b = JSON.parse(b);
  // var obj = JSON.parse("[{'_id':'2018-06-26 11:14:22.122','NAME1':'qw','EMAIL':'qweeqw@s.com','ADDRESS':{'A1':['asdasda','asdasdasdasd','3546546546']},'ID':'47','CONTACTNO':'786567'},{'_id':'2018-06-26 15:00:08.009','NAME1':'Tarun','EMAIL':'asd@we.com','ADDRESS':{'A1':['asdasda','asdasdasdasd','3546546546']},'ID':'55','CONTACTNO':'123123123123'}]");
  console.log(b);
  // b = " '" + b + "' ";
//    console.log(b);
   var c = b.replace(/'/g,"\"");
   console.log(c);
   var d = JSON.parse(c);
   console.log(d);   
   var max_size=d.length;
   console.log(max_size);
   var sta = 0;
   var elements_per_page = 4;
   var limit = elements_per_page;
   goFun(sta,limit);
   function goFun(sta,limit) {
    for (var i =sta ; i < limit; i++) {
      
      var $nr = $('<tr><td>' + d[i].NAME1 + '</td><td>' + d[i].EMAIL  + '</td></tr>');
      table.append($nr);
    }
    }
    $('#nextValue').click(function(){    
      var next = limit;
      console.log(limit<=max_size);
      if( max_size >= next && limit <= max_size) {
      limit = limit+elements_per_page;
      table.empty();
      goFun(next,limit);
      }
    });
    $('#PreeValue').click(function(){
      var pre = limit-(2*elements_per_page);
      if(pre>=0) {
      limit = limit-elements_per_page;
      table.empty();
      goFun(pre,limit); 
      }
    });
  
  });
  