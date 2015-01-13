/********************************
 ** FILE: base.js
 ********************************/
var cancer = cancer || {};

var $j = jQuery;

cancer.filename = function(index){
  var tabs = [
  "total",
  "gender", // formerly: mandatory
  "age", // formerly: discretionary
  "race"]; // formerly: department
  return tabs[index];
}
$j("#save").click(function(){
  $j.ajax({ 
    type: "POST", 
    url: "/save", 
    data: {
      'filename':cancer.filename(cancer.mainNav.currentIndex),
      'contents':cancer.c.getCirclePositions()
    }
  });
  
})


  
function do_everything(){ // formerly cancer.ready = function() {
  var that = this;
  cancer.c = new cancer.Chart();
  cancer.c.init();
  cancer.c.start();
  
  this.highlightedItems = [];

  var currentOverlay = undefined;
  cancer.mainNav = new cancer.ChooseList($j(".cancer-navigation"), onMainChange);
  function onMainChange(evt) {
    var tabIndex = evt.currentIndex;

    if (this.currentOverlay !== undefined) {
      this.currentOverlay.hide();
    };
    if (tabIndex === 0) {
      cancer.c.totalLayout();
      this.currentOverlay = $j("#cancer-totalOverlay");
      this.currentOverlay.delay(300).fadeIn(500);
      $j("#cancer-chartFrame").css({'height':550});
    } else if (tabIndex === 1){
      cancer.c.genderLayout();
      this.currentOverlay = $j("#cancer-genderOverlay");
      this.currentOverlay.delay(300).fadeIn(500);
      $j("#cancer-chartFrame").css({'height':550});
    } else if (tabIndex === 2){
      cancer.c.ageLayout();
      this.currentOverlay = $j("#cancer-ageOverlay");
      this.currentOverlay.delay(300).fadeIn(500);
      $j("#cancer-chartFrame").css({'height':650});
    } else if (tabIndex === 3){
      cancer.c.countryLayout();
      this.currentOverlay = $j("#cancer-countryOverlay");
      this.currentOverlay.delay(300).fadeIn(500);
      $j("#cancer-chartFrame").css({'height':850});
    }
  
  }
  
}

if (!!document.createElementNS && !!document.createElementNS('http://www.w3.org/2000/svg', "svg").createSVGRect){
  $j(document).ready($j.proxy(cancer.ready, this));
} else {
  $j("#cancer-chartFrame").hide();
  // $j("#nytg-error").show();
}
