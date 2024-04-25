import React, { useState } from 'react';
function DirectQueries() {
    const [formState, setFormState] = useState({
        nameValue: '',
        descriptopnValue: '',
        latitudeValue: '',
        longtitudeValue: '',
        timestamoValue: '',
        movementX: '',
        movementY: '',
    });
    const handleInputChange = (event) => {
        const { name, value } = event.target;
        setFormState({ ...formState, [name]: value })
    }
    const handleSubmit = (event) => {
        event.preventDefault(); // handle the form submission event, e.g. make an API call to backend server
        console.log(formState); // for testing
    }
    return (
        <div>
            <h2> Direct Queries</h2>
            <form onSubmit={handleSubmit}>
                <label htmlFor='nameValue'> Name:</label>
                <select name="nameValue" onChange={handleInputChange}>
                    <option value="is">Is</option>
                    <option value="contains">Contains</option>
                    <option value="isnt">Isn't</option>
                </select>
                <input
                    type="text"
                    name="nameValue"
                    placeholder="Enter Name"
                    value={formState.nameValue}
                    onChange={handleInputChange}
                />
                <br />

                <label htmlFor="descriptionValue"> Description:</label>
                <select name="descriptionValue" onChange={handleInputChange}>
                    <option value="is">Is</option>
                    <option value="contains">Contains</option>
                    <option value="isnt">Isn't</option>
                </select>
                <input
                    type="text"
                    name="descriptionValue"
                    placeholder="Enter Description"
                    value={formState.descriptionValue}
                    onChange={handleInputChange}
                />

                {/* Repeat for other inputs */}
                {/* ... */}
                <br />
                <input type="submit" value="Submit Query" />
            </form>
        </div>
    )
}
export default DirectQueries;