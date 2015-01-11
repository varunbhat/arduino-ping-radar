
$(function() {
	$('#container').highcharts({
		chart : {
			polar : true,
			events : {
				load : function() {
					// set up the updating of the chart each second
					var series = this.series[0];
					var ds = [];
					setInterval(function() {
						$.ajax({
							url: "http://localhost:8000/json_data"
						}).done(function(data){
							console.log(data);
							ds = JSON.parse(data);
						});
						series.setData(ds);
						series.redraw();
					}, 50);
				}
			}
		},

		title : {
			text : 'Arduino Radar'
		},

		pane : {
			startAngle : 0,
			endAngle : 360
		},

		xAxis : {
			tickInterval : 45,
			min : 0,
			max : 360,
			labels : {
				formatter : function() {
					return this.value + '°';
				}
			}
		},

		yAxis :  {
			min : 0,
			max : 400
			},

		plotOptions : {
			series : {
				pointStart : 0,
				pointInterval : interval_slice
			},
			column : {
				pointPadding : 2,
				groupPadding : 1
			}
		},

		series : [{
			type : 'area',
			name : 'Line',
			data : ( function() {
					// generate an array of random data
					var data = [],
					    i;

					for ( i = 0; i <= 360; i = i + interval_slice) {
						data.push(10);
					}
					return data;
				}())
		}]
	});
});
