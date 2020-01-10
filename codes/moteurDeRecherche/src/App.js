import React from "react";
import ReactDOM from "react-dom";

import {
  ReactiveBase,
  DataSearch,
  MultiList,
  SelectedFilters,
  ReactiveList,
  RangeSlider
} from "@appbaseio/reactivesearch";
import { Row, Button, Col, Card} from "antd";
import "antd/dist/antd.css";


function renderItem(res, triggerClickAnalytics) {
  var title = ""
  var url = ""
  if (res.raa.length <= 0)
	  title = "Pas un RAA";
  else
	  title = "RAA n° " + res.raa[0];
  
  if (res.taxo.length > 0)
	  var taxo = "Classement taxonomique : ";
	  for (var i=0; i < res.taxo.length && i < 3; i++)
		  taxo += res.taxo[i] + ", ";

  var publi = res.publi.split ("-");
  var date = ""
  if (publi.length === 3)
  	date = "Date de publication: " + publi[2] + "/" + publi[1] + "/" + publi[0];

  return (
    <Row
      onClick={triggerClickAnalytics}
      type="flex"
      gutter={16}
      key={res._id}
      style={{ margin: "20px auto", borderBottom: "1px solid #ededed" }}
    >
      <Col span={24}>
        <h3> <font size="+2">
		{title}
	</font> </h3>
	<div><span className="publi-date">{date}</span> </div>
	<div> {taxo} </div>
      </Col>
      <div style={{ padding: "20px" }}>
        {url ? (
          <Button
            shape="circle"
            icon="link"
            style={{ marginRight: "5px" }}
            onClick={() => window.open(url, "_blank")}
          />
        ) : null}
      </div>
    </Row>
  );
}

const App = () => (
  <ReactiveBase
    app="prefetapp"
    credentials="qr2npidUt:2b829168-09bd-454a-b924-d2fdaeb56c59"
    url="https://scalr.api.appbase.io"
    analytics={true}
    searchStateHeader
  >
    <Row gutter={16} style={{ padding: 20 }}>
      <Col span={5}>
        <Card>
          <MultiList
            componentId="raaList"
	    showCount={false}
            dataField="raa.keyword"
            queryFormat="or"
            sortBy="desc"
            size={10000}
            style={{
              marginBottom: 20
            }}
            title="Références RAA"
          />
	
          <RangeSlider
            componentId="datesPubliSlider"
            dataField="publi.keyword"
            queryFormat="and"
            style={{
              marginBottom: 40
            }}
	    range={{
              start: 1950,
              end: 2050
	    }}
	    rangeLabels={{
              start: "1950",
              end: "2050"
	    }}
            showHistogram={true}
            showFilter={true}
            title="Date de publication"
          />

          <MultiList
            componentId="taxonomieList"
            dataField="taxo.keyword"
            queryFormat="and"
            size={100}
            style={{
              marginBottom: 40
            }}
	    react={{and: [
	      	"raaList",
		"arretesList",
		"datesPubliSlider",
		"searchBar"
	    	]
	    }}
            title="Taxonomie"
          />
          <MultiList
            componentId="arretesList"
            dataField="arretes.keyword"
            queryFormat="and"
            size={100}
            style={{
              marginBottom: 20
            }}
	    react={{and: [
		"taxonomieList", 
	      	"raaList",
		"datesPubliSlider",
		"searchBar"
	    	]
	    }}
            title="Arretes"
          />
        </Card>
      </Col>
      <Col span={18}>
        <DataSearch
          autosuggest={true}
          componentId="searchBar"
	  react={{
	    and: [
	     "taxonomieList", 
	     "raaList",
	     "arretesList",
	     "datesPubliSlider",
	     ]
            }}
          dataField={[
            "raa",
            "publi",
            "arretes",
            "dates",
            "titres",
            "decrets",
            "lois",
            "noms",
            "articles",
            "taxo",
            "lieux",
            "orgs"
          ]}
          fieldWeights={[
            10,
            5,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1,
            1
	  ]}
	  debounce={100}
          fuzziness="AUTO"
          queryFormat="and"
          size={10}
          style={{
            marginBottom: 20
          }}
          title="Recueil Search Engine"
	  renderError={error => (
	      <div>
	      Something went wrong with DataSearch
		<br />
	        Error details
		<br />
	        {error}
		</div>
	   )}
	   sortOptions={["Test", "publi", "asc"]}
        />

        <SelectedFilters
		showClearAll={true}
		clearAllLabel="Clear filters"
	/>
        <div id="result">
          <ReactiveList
            componentId="result"
            dataField="_score"
            pagination={true}
	    loader="Loading Results.."
            react={{
              and: [
		"taxonomieList", 
	      	"raaList",
		"arretesList",
		"datesPubliSlider",
		"searchBar"
		]
            }}
            renderItem={renderItem}
            size={10}
            style={{
              marginTop: 20
            }}
          />
        </div>
      </Col>
    </Row>
  </ReactiveBase>
);

ReactDOM.render(<App />, document.getElementById("root"));
export default App;
