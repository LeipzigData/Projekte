package calendarApi.api;

/**
 * Calendar API implementation for API.Leipzig.
 * 
 * @author Christof Pieloth
 */
public class ApiLeipzig extends CalendarApi {

	private static final String URL = "http://www.apileipzig.de/api/v1";
	private static final String NAME = "API.Leipzig";

	public ApiLeipzig() {
		this(DEFAULT_KEY);
	}

	public ApiLeipzig(String key) {
		super(key);
	}

	@Override
	public String getUrl() {
		return URL;
	}

	@Override
	public String getName() {
		return NAME;
	}

}
