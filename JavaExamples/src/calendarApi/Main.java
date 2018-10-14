package calendarApi;

import java.util.List;

import calendarApi.api.ApiLeipzig;
import calendarApi.api.CalendarApi;
import calendarApi.api.LeipzigData;
import calendarApi.entity.Event;

/**
 * CLI access to a Calendar API.
 * 
 * @author Christof Pieloth
 * 
 */
public class Main {

	/**
	 * Entry point for CLI access.
	 * 
	 * @param args
	 *            CLI arguments: API key
	 */
	public static void main(String[] args) {
		String apiKey;
		if (args.length > 0)
			apiKey = args[0];
		else {
			System.err.println("Please set an API key!");
			apiKey = CalendarApi.DEFAULT_KEY;
		}

		CalendarApi api = null;
		List<Event> events = null;

		api = new ApiLeipzig(apiKey);
		System.out.println("Fetching from " + api.getName() + " ...");
		events = api.getEvents();
		if (events != null) {
			for (Event e : api.getEvents()) {
				System.out.println("--------------------");
				System.out.println(e);
				System.out.println("Venue: ");
				System.out.println(api.getVenue(e.getVenueId()));
			}
		} else {
			System.err.println("No events found!");
		}

		System.out.println("\n##############################\n");

		api = new LeipzigData(apiKey);
		System.out.println("Fetching from " + api.getName() + " ...");
		events = api.getEvents();
		if (events != null) {
			for (Event e : api.getEvents()) {
				System.out.println("--------------------");
				System.out.println(e);
				System.out.println("Venue: ");
				System.out.println(api.getVenue(e.getVenueId()));
			}
		} else {
			System.err.println("No events found!");
		}
	}

}
