package calendarApi.api;

/**
 * Calendar API implementation for LeipzigData.
 * 
 * @author Christof Pieloth
 */
public class LeipzigData extends CalendarApi {

	private static final String URL = "http://ld.data.apileipzig.de";
	private static final String NAME = "LeipzigData";

	public LeipzigData() {
		this(DEFAULT_KEY);
	}

	public LeipzigData(String key) {
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
