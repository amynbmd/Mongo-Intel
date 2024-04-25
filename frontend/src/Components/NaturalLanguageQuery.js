// this components is used to display the direct queries of the user
// it is used in the DirectQueries.js file
// in real-world application, the 'handleSiubmit' function in NaturalLanguageQuery.js should handle the logic fo rwhat happens when the user submit a query. Typically, thhis would involve making an API call to backend server. Can use 'fetch' or libraries 'axios' to make these calls. 
import React from 'react';
import { useState } from 'react';
function NaturalLanguageQuery() {

    const [query, setQuery] = useState(''); // this is the query that the user will enter
    const handleSubmit = (event) => {
        event.preventDefault();
        alert(`Submitting Query: ${query}`);
    }
    //add form submission logic here
    return (
        <form onSubmit={handleSubmit}>
            <h2> Natural Language Query</h2>
            <label htmlFor="natural_language_query"> Enter your query:</label>
            <textarea
                className="queryTextarea"
                name="natural_language_query"
                id="natural_language_query"
                col="50%"
                row="50"
                placeholder="Enter your query here"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
            ></textarea>
            <br />
            <input type="submit" value="Submit Query" />
        </form>

    );
}

export default NaturalLanguageQuery;