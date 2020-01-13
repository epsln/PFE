import React from "react";
import ReactDOM from "react-dom";

import {
  ReactiveBase,
  DataSearch,
  MultiList,
  SelectedFilters,
  ReactiveList,
  RangeSlider,
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
      <div> "Nom local du fichier :" {res.name} </div>
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
            componentId="RAA"
            dataField="raa.keyword"
            queryFormat="or"
	    showCount={false}
            sortBy="desc"
            size={100}
            style={{
              marginBottom: 20
            }}
            title="Références RAA"
          />
          <RangeSlider
            componentId="dates_publi"
            dataField="publi.keyword"
            queryFormat="and"
            size={100}
            style={{
              marginBottom: 40
            }}
            range={{
              start: 1900,
              end: 2050
            }}
            rangeLabels={{
              start: "1900",
              end: "2050"
            }}
            stepValue={1}
            showHistogram={true}
            showFilter={true}
            interval={2}
            title="Dates de publications"
            react={{
              and: ["taxonomie", "raa", "arretes", "search"]
            }}
          />
          <MultiList
            componentId="taxonomie"
            dataField="taxo.keyword"
            queryFormat="and"
            size={100}
            style={{
              marginBottom: 40
            }}
            title="Taxonomie"
            react={{
              and: ["raa", "arretes", "dates_publi", "search"]
            }}
          />
          <MultiList
            componentId="arretes"
            dataField="arretes.keyword"
            queryFormat="and"
            size={100}
            style={{
              marginBottom: 20
            }}
            title="Arretes"
            react={{
              and: ["taxonomie", "raa", "dates_publi", "search"]
            }}
          />
        </Card>
      </Col>
      <Col span={18}>
        <div className="navbar">
          <div className="logo-container">
            <img
                className="app-logo"
                src="https://www.origne53.fr/images/PREFECTURE.jpg"
                alt="LogoPrefeture"
                width="150" 
                height="100"
            />
            <img
                className="app-logo"
                src="https://www.esiea.fr/wp-content/uploads/2016/04/Logo-ESIEA.jpg"
                alt="LogoEsiea"
                width="200" 
                height="100"
                align="right"
            />
          </div>
        </div>
        <DataSearch
          autosuggest={true}
          componentId="search"
          dataField={[
            "raa",
            "publi",
            "taxo",
            "noms",
            "dates",
            "arretes",
            "articles",
            "decrets",
            "lieux",
            "lois",
            "orgs",
            "titres"
          ]}
          fieldWeights={[
            10,
            6,
            6,
            4,
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
          fuzziness={1}
          highlight={false}
          highlightField={[
            "arretes",
            "articles",
            "dates",
            "decrets",
            "lieux",
            "lois",
            "noms",
            "orgs",
            "publi",
            "raa",
            "taxo",
            "titres"
          ]}
          queryFormat="and"
          size={10}
          style={{
            marginBottom: 20
          }}
          title="Receuil Search Engine"
        />

        <SelectedFilters />
        <div id="result">
          <ReactiveList
            componentId="result"
            dataField="_score"
            pagination={true}
            react={{
              and: ["taxonomie", "raa", "arretes", "dates_publi", "search"]
            }}
	    loader="Chargement..."
	    noResults="Pas de resultats correspondants a votre recherche"
            renderItem={renderItem}
            size={12}
            style={{
              marginTop: 20
            }}
            sortOptions={[
                {
                  dataField: "_score",
                  sortBy: "desc",
                  label: "Pertinence"
                },
                {
                  dataField: "publi.keyword",
                  sortBy: "desc",
                  label: "Date de publication (desc)"
                },
                {
                  dataField: "publi.keyword",
                  sortBy: "asc",
                  label: "Date de publication (asc)"
                }
            ]}
          />
        </div>
      </Col>
    </Row>
  </ReactiveBase>
);

ReactDOM.render(<App />, document.getElementById("root"));
export default App;
