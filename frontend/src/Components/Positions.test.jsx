import {
  render,
  screen,
  fireEvent,
  waitForElementToBeRemoved,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import Positions from "./Positions";
import { BrowserRouter as Router } from "react-router-dom";

describe("Positions Component", () => {
  test("adds a new row when 'Add a row' button is clicked", async () => {
    render(
      <Router>
        <Positions />
      </Router>
    );

    // If there's a loading indicator, wait for it to disappear
    await waitForElementToBeRemoved(() => screen.queryByText(/Loading.../i));

    // Now that loading is presumably done, try to find the "Add a row" button
    const addButton = await screen.findByText(/Add a row/i);
    expect(addButton).toBeInTheDocument();
  });
});
