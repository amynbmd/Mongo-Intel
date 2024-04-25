import React from "react";
import { render, fireEvent, waitFor } from "@testing-library/react";
import AreaAnalysis from "./AreaAnalysis";
import axios from "axios";

// Mock axios globally
jest.mock("axios");

describe("AreaAnalysis Component", () => {
  beforeEach(() => {
    // Reset the mocks before each test
    axios.get.mockReset();
  });

  test("updates the query on user input", () => {
    const { getByPlaceholderText } = render(<AreaAnalysis />);
    const inputField = getByPlaceholderText("Empty");
    fireEvent.change(inputField, {
      target: { value: "test query", name: "query" },
    });
    expect(inputField.value).toBe("test query");
  });

  test("submits the form and updates positions based on API response", async () => {
    const mockResponse = {
      data: [
        {
          _id: "1",
          location: { coordinates: [123, 456] },
          name: "Test",
          description: "Test Description",
          timestamp: "Now",
          heading: "North",
          speed: 10,
        },
      ],
    };

    // Mock axios.get specifically for this test
    axios.get.mockResolvedValue(mockResponse);

    const { getByRole, getByPlaceholderText } = render(<AreaAnalysis />);
    const inputField = getByPlaceholderText("Empty");
    fireEvent.change(inputField, {
      target: { value: "test query", name: "query" },
    });

    fireEvent.click(getByRole("button", { name: /search/i }));

    await waitFor(() => {
      expect(axios.get).toHaveBeenCalled();
      // You can add more assertions here to check if the component behaved as expected
    });
  });

  // Additional tests go here
});
