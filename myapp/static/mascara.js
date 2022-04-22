$(document).ready(function(){
    $('.money').mask('000.000.000.000.000,00', {reverse: true});
   

    $("#myForm").submit(function() {
        money = $(".money").val().replace('.', '').replace(',','.');
        $(".money").val(money)
       
      });

    $('.date').mask('00/00/0000');
  
});