import React, { useEffect, useState, useRef } from 'react';
import axios from 'axios';
import { DataGrid } from '@mui/x-data-grid'; //https://mui.com/x/react-data-grid/layout/
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/DeleteOutlined';
import SaveIcon from '@mui/icons-material/Save';
import CancelIcon from '@mui/icons-material/Close';
import { GridRowModes, GridActionsCellItem, GridRowEditStopReasons } from '@mui/x-data-grid';
import { Map, GoogleApiWrapper, Marker } from 'google-maps-react';

const Positions = (props) => {
  const mapStyles = {
    width: '95%',
    height: '80%',
  };
  const baseURL = process.env.REACT_APP_DB_SERVER_URL;
  const positionAPI = `${baseURL}/positions/`;
  const [map, setMap] = useState(null);
  const mapRef = useRef(null);

  useEffect(() => {
    if (rows.length === 0) {
      fetchPositions();
    }

    // if the map exists, assign the map instance to mapRef
    if (mapRef.current && !map) {
      const initializedMap = new props.google.maps.Map(mapRef.current, {
        center: { lat: -34.397, lng: 150.644 },
        zoom: 8,
      });
      setMap(initializedMap);
    }
  }, [mapRef, map, props.google.maps.Map]);

  const handleEditClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.Edit } });
  };

  const handleSaveClick = (id) => () => {
    setRowModesModel({ ...rowModesModel, [id]: { mode: GridRowModes.View } });
  };

  const handleDeleteClick = (id) => async () => {
    setRows(rows.filter((row) => row.id !== id));

    if (id != 0) {
      const response = await axios.delete(positionAPI + id);
    }
  };

  const handleCancelClick = (id) => () => {
    setRowModesModel({
      ...rowModesModel,
      [id]: { mode: GridRowModes.View, ignoreModifications: true },
    });

    if (id == 0) {
      setRows(rows.filter((row) => row.id !== id));
    } else {
      const editedRow = rows.find((row) => row.id === id);
      if (editedRow.isNew) {
        setRows(rows.filter((row) => row.id !== id));
      }
    }
  };

  const processRowUpdate = async (newRow) => {
    let updatedRow = { ...newRow, isNew: false };
    const location = updatedRow.location.split(',').map((s) => Number(s));

    const obj = {
      name: updatedRow.name,
      entity_id: updatedRow.entity_id,
      description: updatedRow.description,
      timestamp: updatedRow.timestamp,
      coordinates: location,
      heading: updatedRow.heading,
      speed: updatedRow.speed,
    };
    updatedRow.coordinates = location;

    if (updatedRow.id == 0) {
      const response = await axios.post(positionAPI, obj);
      updatedRow.id = response.data._id;
      
      setRows([...rows.filter((row) => row.id != 0), updatedRow]);
    } else {
      const response = await axios.put(positionAPI + updatedRow.id, obj);

      setRows(rows.map((row) => (row.id === updatedRow.id ? updatedRow : row)));
    }

    return updatedRow;
  };

  const handleRowModesModelChange = (newRowModesModel) => {
    setRowModesModel(newRowModesModel);
  };

  const handleRowEditStop = (params, event) => {
    if (params.reason === GridRowEditStopReasons.rowFocusOut) {
      event.defaultMuiPrevented = true;

      console.log(rows);
    }
  };

  let [rows, setRows] = useState([]);
  const [rowModesModel, setRowModesModel] = useState({});
  const columns = [
    { field: 'id', headerName: 'ID', flex: 2 },
    { field: 'entity_id', headerName: 'Entity ID', flex: 1, editable: true },
    { field: 'name', headerName: 'Name', flex: 1, editable: true },
    { field: 'description', headerName: 'Description', flex: 2, editable: true },
    { field: 'timestamp', headerName: 'Datetime', flex: 2, editable: true, type: 'dateTime' },
    { field: 'location', headerName: 'Location', flex: 2, editable: true },
    { field: 'heading', headerName: 'Heading', flex: 1, editable: true },
    { field: 'speed', headerName: 'Speed', flex: 1, editable: true },
    {
      field: 'actions',
      type: 'actions',
      headerName: 'Actions',
      width: 100,
      cellClassName: 'actions',
      getActions: ({ id }) => {
        const isInEditMode = rowModesModel[id]?.mode === GridRowModes.Edit;

        if (isInEditMode) {
          return [
            <GridActionsCellItem
              icon={<SaveIcon />}
              label="Save"
              sx={{
                color: 'primary.main',
              }}
              onClick={handleSaveClick(id)}
            />,
            <GridActionsCellItem icon={<CancelIcon />} label="Cancel" className="textPrimary" onClick={handleCancelClick(id)} color="inherit" />,
          ];
        }

        return [<GridActionsCellItem icon={<EditIcon />} label="Edit" className="textPrimary" onClick={handleEditClick(id)} color="inherit" />, <GridActionsCellItem icon={<DeleteIcon />} label="Delete" onClick={handleDeleteClick(id)} color="inherit" />];
      },
    },
  ];

  const processData = async (data) => {
    if (rows.length === 0) {
      rows = data.position_docs.map((position) => {
        return {
          id: position._id,
          entity_id: position.entity_id,
          name: position.name,
          description: position.description,
          timestamp: new Date(position.timestamp),
          location: `${position.location.coordinates[0]}, ${position.location.coordinates[1]}`,
          coordinates: position.location.coordinates,
          heading: position.heading,
          speed: position.speed,
        };
      });

      setRows(rows);

      console.log(rows);
    }
  };

  const fetchPositions = async () => {
    try {
      const response = await axios.get(positionAPI);
      processData(response.data);
    } catch (error) {
      console.error('Error fetching position data', error);
    }
  };

  useEffect(() => {
    if (rows.length === 0) {
      fetchPositions();
    }
  });

  const handleAddRow = () => {
    const newRow = {
      description: null,
      id: '0',
      entity_id: 0,
      location: null,
      coordinates: [0,0],
      name: null,
      timestamp: new Date(),
      heading: null,
      speed: null,
    };

    setRows([newRow, ...rows]);
    setRowModesModel({ ...rowModesModel, [newRow.id]: { mode: GridRowModes.Edit } });
  };

  return (
    <div className="mt-4 ps-5 pe-5">
      <Box sx={{ height: '100%', width: '100%' }}>
        <div style={{ paddingBottom: '20px' }}>
          <Button variant="contained" size="small" onClick={handleAddRow}>
            Add a row
          </Button>
        </div>
        <Box>
          <DataGrid
            rows={rows}
            columns={columns}
            editMode="row"
            rowModesModel={rowModesModel}
            onRowModesModelChange={handleRowModesModelChange}
            // onRowEditStop={handleRowEditStop}
            processRowUpdate={processRowUpdate}
            initialState={{
              pagination: {
                paginationModel: {
                  pageSize: 25,
                },
              },
            }}
            pageSizeOptions={[25, 50, 100]}
            // checkboxSelection
            disableRowSelectionOnClick
          />
        </Box>
      </Box>

      <div style={{paddingTop: "20px"}}>
        <Map
          google={props.google}
          zoom={11}
          style={mapStyles}
          initialCenter={{ lat: 38.8462, lng: -77.30637 }} // Default center is fairfax city
        >
          {rows.length > 0 &&
            rows.map((position) => {

              if (position.id != '0') {
                return (
                  <Marker
                    key={position.id}
                    position={{
                      lat: position.coordinates[1],
                      lng: position.coordinates[0],
                    }}
                    title={
                      'Name: ' + position.name + '\n' +
                      'Description: ' + position.description + '\n' +
                      'Datetime: ' + position.timestamp + '\n' + 
                      'Longtitude: ' + position.coordinates[0] +'\n' + 
                      'Latitude: ' + position.coordinates[1] +'\n' + 
                      'Heading: '+ position.heading + '\n' + 
                      'Speed: ' + position.speed + ' km/h'}
                  />
                );
              }

            })}
        </Map>
      </div>
    </div>
  );
};

export default GoogleApiWrapper({
  apiKey: process.env.REACT_APP_GOOGLE_API_KEY,
})(Positions);
