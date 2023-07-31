class Player {
	tag: string;
	name: string;
	nameColor: string;
	role: string;
	trophies: number;
	icon: {
		id: number;
	};
}

class Paging {
	cursors: {};
}

export declare type PlayersData = {
	members: Player[];
	paging: Paging;
};
