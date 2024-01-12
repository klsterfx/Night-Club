import React from 'react';

export default function ClubDetailsBox(props) {
    if (props.club[5] <  props.club[4]){
      return <div className="box"> 
              <font size="+3">{props.club[0]} </font><br/> 
              Location:{props.club[1]} <br/>
              Music:{props.club[2]} <br/>
              Capacity:{props.club[3]} <br/>
              Yellow:{props.club[4]} <br/> 
              Count:{props.club[5]} <br/> 
              Welcome!</div>;
    }
    else if (props.club[5] < props.club[3]){
      return <div className="boxYellow"> 
              <font size="+3">{props.club[0]} </font><br/> 
              Location:{props.club[1]} <br/>
              Music:{props.club[2]} <br/>
              Capacity:{props.club[3]} <br/>
              Yellow:{props.club[4]} <br/> 
              Count:{props.club[5]} <br/> 
              Warn the bouncers!</div>;
    }
    else {
      return <div className="boxRed">  
              <font size="+3">{props.club[0]} </font><br/> 
              Location:{props.club[1]} <br/>
              Music:{props.club[2]} <br/>
              Capacity:{props.club[3]} <br/>
              Yellow:{props.club[4]} <br/> 
              Count:{props.club[5]} <br/> 
              No more entry!</div>;
    }
  }
  