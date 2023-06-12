import axios from "axios"; // Import axios for making HTTP requests

const url = "http://54.227.172.163:3000/"; //backend url

export const getData = async () => {
  try {
    const response = await axios.get(url + "data");
    const jsonData = await response.data;
    return jsonData;
  } catch (error) {
    console.error("Error:", error);
    throw error;
  }
}; //function to get SPAM Data from backend

export const resolveData = async (id) => {
  try {
    const newData = { ticketState: "CLOSED" };
    const response = await axios.put(url + `reports/${id}`, newData);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    // Handle the error
  }
}; //function to resolve SPAM Data from backend

export const blockData = async (id, state) => {
  try {
    const newData = { ticketState: state };
    const response = await axios.put(url + `block/${id}`, newData);
    console.log(response.data);
    return response.data;
  } catch (error) {
    console.error("Error:", error);
    // Handle the error
  }
}; //function to block/unblock SPAM Data from backend