import axios from 'axios';
export const getAIMessage = async (userQuery) => {
  try {
    const response = await axios.get('http://localhost:5000/getapimessage',
      {params: {input: userQuery}});
    console.log(response.data["role"]);
    
    const message = {
      role: response.data["role"],
      content: response.data["content"]
    };

    return message;

  } catch (error) {
    console.error(error);
    return {
      role: 'error',
      content: 'There was an error retrieving the message.'
    };
  }
};
