import axios from "axios";

export const uploadVideo = async (formData: FormData) => {
  return axios.post("http://localhost:5000/upload", formData, {
    headers: {
      "Content-Type": "multipart/form-data",
    },
  });
};
