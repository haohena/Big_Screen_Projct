var timestamp = Date.parse(new Date());
console.log(timestamp)
window.onload=function(){
	var btn_1=document.getElementById("btn_1");
	var close=document.getElementsByClassName("close");
	var form_1=document.getElementsByClassName("form_1");
	btn_1.addEventListener('click',function(){
		form_1[0].className="form_1 open";	
	})
	close[0].addEventListener('click',function(){
		form_1[0].className="form_1";
	})

}

var cap_num_info = 200
function submit_info(){
	var cap_num = document.getElementById('cap_num')
	if(Number(cap_num.value)>0)
	{
		cap_num_info = Number(cap_num.value)
		alert('成功修改为：'+cap_num.value)
	}
}
$(function(){
	$("body").click(function(){
		$(".depo_down").slideUp();
	})
	$(".depot").click(function(e){
		e.stopPropagation();
		if($(this).hasClass("active")){
			$(this).removeClass("active");
			$(".depo_down").slideUp();
		}else{
			$(this).addClass("active");
			$(".depo_down").slideDown();
		}
	})
	$(".depo_down li").click(function(){
		var tex=$(this).text();
		$(".depot input").val(tex);
	})
	var myChart1 =echarts.init(document.getElementById('chart_1'));
	 var option1 = {
	 	// backgroundColor: '#1b1e25',
	    tooltip: {
	      enterable:true,
          trigger: 'axis'
		},
        legend:{
            data:['参观人数','实时舱内人数'],
            textStyle:{
                color:'white',
                fontSize:15
            }
        },
	    grid: {
	        left: '3%',
	        right: '3%',
	        top: '10%',
	        bottom:"2%",
	        containLabel: true
	    },
	    xAxis : [
	        {
        	   axisLine:{
                  lineStyle:{
                    color:'#1b1e25',
                    width:1,//突出显示
                  }
               },
	            type : 'category',
	            boundaryGap : false,
	            data : ['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23']  //左图横轴  时间
	        }
	    ],
	    yAxis : [
	        {
	        	splitLine:{
		            lineStyle:{
		                color: '#21242b',
		            }
		        },
	            type : 'value',
	            axisLine:{
                    lineStyle:{
                        color:'#1b1e25',
                        width:1,//突出显示
                    }
                }
	        }
	    ],
	    series : [
	        {
	            name:'参观人数',
	            type:'line',
	            symbol:'none',
	            data:['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] ,//左图纵轴  累计参观人数
	            smooth: true,
	            itemStyle : {
                    normal : {
                        lineStyle:{
                            color:'#4f3c06'
                        }
                    }
                },
                areaStyle: {
                    opacity: 0.5
                  },
	        },
            {
	            name:'实时舱内人数',
	            type:'line',
	            symbol:'none',
	            data:['0','1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23'] ,  //左图纵轴  实时人数/小时
	            smooth: true,
	            itemStyle : {
                    normal : {
                        lineStyle:{
                            color:'#34a66b'
                        }
                    }
                },
                areaStyle: {
                    opacity: 0.5
                  },
	        },
	    ]
	};
	var myChart3 =echarts.init(document.getElementById('chart_3'));
	var option3 = {
		grid: {
	        left: '3%',
	        right: '3%',
	        top: '10%',
	        bottom:"2%",
	        containLabel: true
	    },
		// backgroundColor: '#1b1e25',
	    tooltip: {
	        trigger: 'item',
	        formatter: " {b}:{d}%",
	    },
	    legend: {
	        orient: 'vertical',
	        right: 10,
            y:'center',
            textStyle: {
		        color: 'white',
                fontSize:15,
		    },
            itemWidth: 30,
            itemHeight: 30,
	        data:['实时舱内人数','还可容纳人数'],
	        formatter: function (params) {
			   for (var i = 0; i < option3.series[0].data.length; i++) {
			       if (option3.series[0].data[i].name == params) {
			           return params +":"+ option3.series[0].data[i].value;
			       }
			   }
			}
	    },
	    series: [
	        {
	            name:'',
	            type:'pie',
                datasetIndex: 1,
	            radius: ['50%', '70%'],
	            avoidLabelOverlap: false,
                label : {
                    　　　　normal : {
                    　　　　　　formatter: '{b}:{c}({d}%)',
                    　　　　　　textStyle : {
                    　　　　　　　　fontWeight : 'normal',
                    　　　　　　　　fontSize : 15,
                                  color:'white',
                    　　　　　　}
                    　　　　}
                    　　},
	            labelLine:{
                    normal:{
                        length:15,     // 指示线宽度
                        lineStyle: {
                            color: "black"    // 指示线颜色  
                        }
                    },
                },
	            data:[
                    {value:200, name:'还可容纳人数'},  //右图饼图  剩余空间
	                {value:0, name:'实时舱内人数'},   //右图饼图  占用空间
	            ], 
                // roseType: 'angle', 
			    itemStyle: {
                    emphasis: {
                        shadowBlur: 10,
                        shadowOffsetX: 0,
                        shadowColor: 'rgba(0, 0, 0, 0.5)'
                     },
                    normal:{
                        color:function(params) {
                        var colorList = [
                            '#2e684d', '#ffc00a','#7d714a', '#447cb7', '#be4868', '#4dc892', '#efbb43',
                            ];
                            return colorList[params.dataIndex]
                         }
                    }
              }
	        }
	    ]
	};
	var setoption=function(){
		myChart1.setOption(option1);//数据统计
		myChart3.setOption(option3);//饼图统计
	}
	 setoption()
	$(window).resize(function(){
		myChart1.resize();
		myChart3.resize();
	})

	function refreshData() {
		$.ajax({
			type:"get",
			url:"http://169.254.8.90:8086/getflow",
			dataType:'json',
			success:function(json){
				// console.log(json)
				// console.log(typeof(json['hour_in']))
				$('#in').text(json['day_in'])
				$('#stay').text(json['day_stay'])
				$('#inmax').text(json['inmax'])
				$('#staymax').text(json['staymax'])
				$('#month').text(json['month'])
				$('#monthmax').text(json['monthmax'])

				// console.log(option1['xAxis'][0]['data'])  //还可以容纳
				// console.log(option1['series'][0]['data'])  //实时
				// console.log(option1['series'][1]['data']) 
				option3['series'][0]['data'][1]['value'] = json['day_stay']
				capacity = cap_num_info - json['day_stay']
				if (capacity <0)
					option3['series'][0]['data'][0]['value'] = 0
				else
					option3['series'][0]['data'][0]['value'] = capacity

				option1['series'][0]['data'] = json['hour_in']
				option1['series'][1]['data'] = json['hour_stay']
				setoption()
			},
			error:function(){
				console.log('111')
			}
		})
		// 这里是刷新数据的代码
		// console.log("数据已刷新");
	  }
	  
	  function startRefresh() {
		var now = new Date(); // 获取当前时间
		var nextRefresh = new Date(now.getFullYear(), now.getMonth(), now.getDate(), now.getHours(), now.getMinutes()+1, 0); // 设置下一个刷新时间为今天的12点
	  
		var timeToRefresh = nextRefresh.getTime() - now.getTime(); // 计算距离下一个刷新时间还有多长时间（单位：毫秒）
		setTimeout(function() {
		  refreshData(); // 刷新数据
		  setInterval(refreshData,500); // 设置每隔24小时刷新一次数据24 * 60 * 60 * 1000
		}, timeToRefresh);
	  }
	  
	  startRefresh();
})
