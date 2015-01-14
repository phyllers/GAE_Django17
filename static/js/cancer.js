d3.json("https://isb-cgc.appspot.com/_ah/api/gae_endpoints/v1/fmdata?disease_code=BLCA", function (error,json) {
    if (error) {
        d3.select('#cancer-chartCanvas')
            .html('<p>HTTP Error ' + error['status'] + ': ' + error['statusText']+'</p>');
        d3.select('#cancer-overlays').style("display", "none");
        return console.warn(error);
    }
    cancer.mutation_array_data = json['items'];
    do_everything();
});



/********************************
 ** FILE: chart.js
 ********************************/

var cancer = cancer || {};

cancer.Chart = function(){

  return {
    $j : jQuery,
    //defaults
    width           : 970,
    height          : 850,
    groupPadding    : 10,
    
    //will be calculated later
    boundingRadius  : null,
    maxRadius       : null,
    centerX         : null,
    centerY         : null,
        
    //d3 settings
    defaultGravity  : 0.1,
    defaultCharge   : function(d){
                        if (d.value < 0) {
                          return 0
                        } else {
                          return -Math.pow(d.radius,2.0)/8 
                        };
                      },
    links           : [],
    nodes           : [],
    positiveNodes   : [],
    force           : {},
    svg             : {},
    circle          : {},
    gravity         : null,
    charge          : null,
    ageTickValues: [20, 30, 40, 50, 60, 70, 80],
    categorizeAge: function(c){ // formerly 2012-2013 change, now age at diagnosis
                        if (isNaN(c)) { return 0;
                        } else if ( c <= 20) { return 1;
                        } else if ( c <= 30){ return 2;
                        } else if ( c <= 40){ return 3;
                        } else if ( c <= 50){ return 4;
                        } else if ( c <= 60){ return 5;
                        } else if ( c <= 70){ return 6;
                        } else if ( c <= 80){ return 7;
                        } else if ( c <= 90){ return 8;
                        } else { return 0; } // any other cases
                      },
    fillColorAge    : d3.scale.ordinal().domain([8,7,6,5,4,3,2,1,0]).range(["#19022a", "#43013a", "#5f0046", "#9e002f", "#ce1129", "#f6441a", "#f68617", "#ffa61e", "#969696"]),
    strokeColorAge  : d3.scale.ordinal().domain([8,7,6,5,4,3,2,1,0]).range(["#4F3D5C", "#52394E", "#470235", "#780024", "#961223", "#BD3515", "#C46C14", "#D48A19", "#5E5E5E"]),
    
    getFillColor    : null,
    getStrokeColor  : null,
    pFormat         : d3.format("+.1%"), // not necessary for cancer?
    pctFormat       : function(){return false}, // not necessary for cancer?
    // tickChangeFormat: d3.format("+%"), // not necessary for cancer
    simpleFormat    : d3.format(","), // not necessary for cancer?
    simpleDecimal   : d3.format(",.2f"),

    bigFormat       : function(n){return cancer.formatNumber(n*1000)}, // not necessary for cancer
    nameFormat      : function(n){return n},
  
    rScale          : d3.scale.pow().exponent(0.5).domain([0,3600]).range([1,50]), // calculate range max from total value
    radiusScale     : null,
    ageScale        : d3.scale.linear().domain([0,90]).range([850,180]), //.clamp(true), 
    sizeScale       : d3.scale.linear().domain([0,110]).range([0,1]),
    groupScale      : {},


    
    //data settings
    tumorWeightDataColumn   : 'tumor_weight', // 'N:SAMP:tumor_weight:::::',
    raceDataColumn          : 'race', // 'C:CLIN:race:::::',
    countryDataColumn       : 'country', // C:CLIN:country:::::',
    genderDataColumn        : 'gender', // C:CLIN:gender:::::',
    ageDataColumn           : 'age_at_initial_pathologic_diagnosis', // N:CLIN:age_at_initial_pathologic_diagnosis:::::',
    barcodeDataColumn       : 'sample', // M:CLIN+SAMP+GNAB',
    histologicalColumn      : 'histological_type', // C:CLIN:histological_type:::::',
    data                    : cancer.mutation_array_data.filter(function(e){ return e['disease_code'] === 'BLCA'}), // custom filter later {return e['M:CLIN+SAMP+GNAB'] === 'TCGA-CF-A1HS-01'}),//
    categoryPositionLookup  : {},
    categoriesList          : [],
    
    // 
    // 
    // 
    init: function() {
      var that = this;
      
      this.pctFormat = function(p){
        if (p === Infinity ||p === -Infinity) {
          return "N.A."
        } else {
          return that.pFormat(p)
        }       
      }

      this.titleFormat = function toTitleCase(str) {
          return str.replace(/\w\S*/g, function(txt){return txt.charAt(0).toUpperCase() + txt.substr(1).toLowerCase();});
      }
      
      this.radiusScale = function(n){
        n = parseFloat(n);
        if (!parseFloat(n)){
          n = 1;
        }
        return that.rScale(Math.abs(n)); 
      };
      this.getStrokeColor = function(d){
        return that.strokeColorAge(d.ageCategory);
      };
      this.getFillColor = function(d){
        return that.fillColorAge(d.ageCategory);
      };
      this.getMouseOverText = function(d){
        var clinical_data = d.gender || '';
        clinical_data += d.race ? (clinical_data === '' ? '': ', ') + d.race : '';
        clinical_data += d.age ? (clinical_data === '' ? '': ', ') + d.age + ' years old at first diagnosis' : '';
        return clinical_data;

      }

  
      // Builds the nodes data array from the original data 
      // and calculates total value and makes categoriesList
      this.totalValue = 0;
      for (var i=0; i < this.data.length; i++) {
        var n = this.data[i];
        var out = {
          sid: n[this.barcodeDataColumn],
          radius: this.radiusScale(n[this.tumorWeightDataColumn]),
          group: (n[this.countryDataColumn] != 'None') ? this.titleFormat(n[this.countryDataColumn].replace(/_/g, ' ')) : null,
          age: (n[this.ageDataColumn] != 'None') ? n[this.ageDataColumn] : null,
          ageCategory: this.categorizeAge(n[this.ageDataColumn]),
          value: (n[this.tumorWeightDataColumn] != 'NA') ? n[this.tumorWeightDataColumn] : null,
          name: (n[this.ageDataColumn] != 'None') ? n[this.histologicalColumn].replace(/_/g, ' ') : 'None specified',
          gender: (n[this.genderDataColumn] != 'None') ? this.titleFormat(n[this.genderDataColumn]) : null,
          race: (n[this.raceDataColumn] != "None") ? this.titleFormat(n[this.raceDataColumn].replace(/_/g, ' ')) : null,
          x:Math.random() * this.width,
          y:Math.random() * this.height
        }
        this.nodes.push(out);
        if (this.categoriesList.indexOf(out.group) < 0) {
          this.categoriesList.push(out.group);
        }
        this.totalValue += parseFloat(n[this.tumorWeightDataColumn]);
      };

      this.categoriesList.sort();
      this.boundingRadius = this.radiusScale(this.totalValue);
      this.centerX = this.width / 2;
      this.centerY = 300;

      //calculates positions of the country category clumps
      //it is probably overly complicated
      // [fill this in later]
      // var columns = [4, 7, 9, 9]
      // rowPadding = [150, 100, 90, 80, 70],
      // rowPosition = [220, 450, 600, 720, 817],
      // rowOffsets = [130, 80, 60, 45, 48]
      currentX = 0,
      currentY = 0;


      this.groupScale = d3.scale.ordinal().domain(this.categoriesList).rangePoints([0,1]);
      

      // age graph
      this.svg = d3.select("#cancer-chartCanvas").append("svg:svg")
        .attr("width", this.width);
      
        for (var i=0; i < this.ageTickValues.length; i++) {
          d3.select("#cancer-ageOverlay").append("div")
            .html("<p>"+this.ageTickValues[i]+"</p>")
            .style("top", this.ageScale(this.ageTickValues[i])+'px')
            .classed('cancer-ageTick', true)
        };
        
      // to do: dynamically calculate cy attributes based on radiusScale and/or totalValue
      d3.select("#cancer-scaleKey").append("circle")
        .attr('r', this.radiusScale(1000))
        .attr('class',"cancer-scaleKeyCircle")
        .attr('cx', 30)
        .attr('cy', 30);
      d3.select("#cancer-scaleKey").append("circle")
        .attr('r', this.radiusScale(100))
        .attr('class',"cancer-scaleKeyCircle")
        .attr('cx', 30)
        .attr('cy', 50);
      d3.select("#cancer-scaleKey").append("circle")
        .attr('r', this.radiusScale(10))
        .attr('class',"cancer-scaleKeyCircle")
        .attr('cx', 30)
        .attr('cy', 55);

      
      // var countryOverlay = $j("#cancer-countryOverlay")
      // for (var i=0; i < country_category_data.length; i++) {   
      // };



      // This is the every circle
      this.circle = this.svg.selectAll("circle")
          .data(this.nodes, function(d) { return d.sid; });

      this.circle.enter().append("svg:circle")
        .attr("r", function(d) { return 0; } )
        .style("fill", function(d) { return that.getFillColor(d); } )
        .style("stroke-width", 1)
        .attr('id',function(d){ return 'cancer-circle'+d.sid })
        .style("stroke", function(d){ return that.getStrokeColor(d); })
        .on("mouseover",function(d,i) { 
          var el = d3.select(this)
          var xpos = Number(el.attr('cx'))
          var ypos = (el.attr('cy') - d.radius - 10)
          el.style("stroke","#000").style("stroke-width",3);
          d3.select("#cancer-tooltip").style('top',ypos+"px").style('left',xpos+"px").style('display','block');
          d3.select("#cancer-tooltip .cancer-name").text(d.group); // used to be html(d.name);
          d3.select("#cancer-tooltip .cancer-gender").html(that.getMouseOverText(d));
          d3.select("#cancer-tooltip .cancer-country").html(d.name); // used to be text(d.group);
          d3.select("#cancer-tooltip .cancer-value").html(d.value ? d.value +" g" : 'No tumor weight data');
        })
        .on("mouseout",function(d,i) { 
          d3.select(this)
          .style("stroke-width",1)
          .style("stroke", function(d){ return that.getStrokeColor(d); })
          d3.select("#cancer-tooltip").style('display','none')
        });
      
            
      this.circle.transition().duration(2000).attr("r", function(d){return d.radius})


    }, // end init

    start: function() {
      var that = this;

      this.force = d3.layout.force()
        .nodes(this.nodes)
        .size([this.width, this.height])     
      // this.circle.call(this.force.drag)
    },

    totalLayout: function() {
      var that = this;
      this.force
        .gravity(-0.01)
        .charge(that.defaultCharge)
        .friction(0.9)
        .on("tick", function(e){
          that.circle
            .each(that.totalSort(e.alpha))
            .each(that.buoyancy(e.alpha))
            .attr("cx", function(d) { 
              return d.x; 
            })
            .attr("cy", function(d) { 
              return d.y; 
            });
        })
        .start();   
    },

    genderLayout: function(){
      var that = this;
      this.force
        .gravity(0)
        .friction(0.9)
        .charge(that.defaultCharge)
        .on("tick", function(e){
          that.circle
            .each(that.genderSort(e.alpha))
            .each(that.buoyancy(e.alpha))
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
        })
        .start();
    },
    ageLayout: function(){
      var that = this;
      this.force
        .gravity(0)
        .charge(0)
        .friction(0.2)
        .on("tick", function(e){
          that.circle
            .each(that.ageSort(e.alpha))
            .attr("cx", function(d) { return d.x; })
            .attr("cy", function(d) { return d.y; });
        })
        .start();
    },
    countryLayout: function(){},


    // ----------------------------------------------------------------------------------------
    // FORCES
    // ----------------------------------------------------------------------------------------
    
    // 
    // 
    // 
    // 
    totalSort: function(alpha) {
      var that = this;
      return function(d){
        var targetY = that.centerY;
        var targetX = that.width / 2;
             
        d.y = d.y + (targetY - d.y) * (that.defaultGravity + 0.02) * alpha;
        d.x = d.x + (targetX - d.x) * (that.defaultGravity + 0.02) * alpha;
      };
    },

    // 
    // 
    // 
    buoyancy: function(alpha) {
      var that = this;
      return function(d){              
          var targetY = that.centerY - (d.ageCategory) * that.boundingRadius;
          d.y = d.y + (targetY - d.y) * (that.defaultGravity) * alpha * alpha * alpha * 100;
      };
    },

    // 
    // 
    // 
    genderSort: function(alpha) {
      var that = this;
      return function(d){
        var targetY = that.centerY;
        var targetX = 0;     
        
        if (d.gender === 'Female') {
          targetX = 600
        } else if (d.gender === 'Male') {
          targetX = 400
        } else { // samples without gender data go off screen -- can change this
          targetX = -300 + Math.random()* 100;
        };
        
        d.y = d.y + (targetY - d.y) * (that.defaultGravity) * alpha * 1.1
        d.x = d.x + (targetX - d.x) * (that.defaultGravity) * alpha * 1.1
      };
    },

    // 
    // 
    // 
    ageSort: function(alpha) {
      var that = this;
      return function(d){
        var targetY = that.height / 2;
        var targetX = 0;
       
        if (d.age) {
          targetY = that.ageScale(d.age);
          targetX = 100 + that.groupScale(d.group)*(that.width - 120);
          if (isNaN(targetY)) {targetY = that.centerY}; // for samples without age data
          if (targetY > (that.height-80)) {targetY = that.height-80}; //?
          if (targetY < 80) {targetY = 80};
          
        } else { // samples without age data go offscreen -- can change this
          targetX = -300 + Math.random()* 100;
          targetY = d.y;
        };
        
        d.y = d.y + (targetY - d.y) * Math.sin(Math.PI * (1 - alpha*10)) * 0.2
        d.x = d.x + (targetX - d.x) * Math.sin(Math.PI * (1 - alpha*10)) * 0.1
      };
    },

  } // end return
} // end Chart object





/********************************
 ** FILE: ChooseList.js
 ********************************/


cancer.ChooseList = function(node, changeCallback) {
  this.container = $j(node);
  this.selectedNode = null;
  this.currentIndex = null;
  this.onChange = changeCallback;
  this.elements = this.container.find('li');
  this.container.find('li').on('click',$j.proxy(this.onClickHandler, this));
  this.selectByIndex(0);
};

cancer.ChooseList.prototype.onClickHandler = function(evt) {
  evt.preventDefault();
  this.selectByElement(evt.currentTarget);
};


cancer.ChooseList.prototype.selectByIndex = function(i) {
  this.selectByElement(this.elements[i])
};


cancer.ChooseList.prototype.selectByElement = function(el) {
  if (this.selectedNode) {
    $j(this.selectedNode).removeClass("selected");
  };
  $j(el).addClass("selected");
  for (var i=0; i < this.elements.length; i++) {
    if (this.elements[i] === el) {
      this.currentIndex = i;
    }
  };
  this.selectedNode = el;
  this.onChange(this);
};